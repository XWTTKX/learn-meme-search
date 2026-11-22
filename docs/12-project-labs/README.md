# 12 · 项目实战：从可解释 BM25 做到多路检索对照

> 实战按三个里程碑推进，每一步都有产物和验收。**里程碑一和二的教学版可以直接运行**。第三步要你准备授权图片和验证集，不宣称仓库替你完成了真实图文评测。

## 12.1 先写一张项目需求卡

你在做一个类似聊天内表情检索的小应用：短词需要找原台词，也能用口语找表达相同心情的图。最小可交付形态不是先做网页，而是：输入一条中文查询，返回有稳定 ID 的一组结果，能解释它们从哪来，以及是否满足单条和全量评测。

| 功能 | 输入 | 输出 | 通过条件 |
|---|---|---|---|
| 词法基线 | 文字标签与查询 | ID、分数、单词贡献 | 能手算两张图的排名 |
| 图文候选/模拟路 | 图片与中文字 | 图文名次或有清晰标记的模拟名次 | 排名输出 ID 与图库一致 |
| 融合 | 两路 ID 榜、不需要原始分数 | 有序唯一 ID | 同分稳定、可解释错误可复现 |
| 评测 | 查询、标签、候选池及 K | 四个指标及无答案信息 | 正例分母与展示预算明示 |
| 诊断结果 | 失败案例 | 推断、复现、单变量修正 | 可以由他人沿同样命令复核 |

```text
交付顺序
  阶段 A：BM25 验证和诊断
       │ 保存一条真实的评分追踪
       ▼
  阶段 B：两路融合和对照
       │ 保存一条召回失败、一条融合失败、一条无答案
       ▼
  阶段 C：授权实图和模型
       │ 冻结标注与参数，跑同样的对照
       ▼
  项目总结：证据、取舍、尚未完成的事情
```

## 12.2 里程碑 A：跑通一条可手算的基线

### 步骤 A1：运行并保存结果

```bash
mkdir -p outputs
python3 scripts/trace_search.py '疲惫' --positive m01 --positive m08 --k 1 > outputs/fatigue-base.json
python3 scripts/trace_search.py '疲惫' --positive m01 --positive m08 --k 1 --b 0 > outputs/fatigue-no-length.json
```

验收：默认 m08 第一、关闭长度修正 m01 第一。Recall 都是 .5；HitRate、MRR、NDCG 都是 1。报告此对照的重点是**结果变化与指标变化不等价**，而非宣称某个 b 更好。

### 步骤 A2：亲手消除一种词法失败

复刻一份教学语料，只在 m01 的标签里增加「累成狗」：

```bash
python3 - <<'PY'
import json
from pathlib import Path
source = Path("data/sample/memes.json")
docs = json.loads(source.read_text(encoding="utf-8"))
for doc in docs:
    if doc["id"] == "m01":
        doc["text"] += " 累成狗"
Path("outputs/memes-added-label.json").write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
PY
python3 scripts/trace_search.py '累成狗' --positive m01 --positive m08 --k 2
python3 scripts/trace_search.py '累成狗' --positive m01 --positive m08 --k 2 --data outputs/memes-added-label.json
```

预期第一条无结果；第二条 m01 匹配并进入 TopK，但 m08 仍缺失。由此能证明「加别名」解决了哪条准确 query，但不能假装它泛化到所有同义词。对正式数据不要根据测试查询逐条补词，再用同一测试集总结提升；这个操作是教学干预，验证因果链用。

## 12.3 里程碑 B：接两路候选，先诊断再调融合

运行 `python3 scripts/fusion_lab.py > outputs/fusion.jsonl`。两路的输入含义不同：词法来自真实 BM25，视觉榜是手填。读输出时按以下顺序核对：

| 查询 | 词法候选 | 图文候选（手填） | 要从输出找的证据 |
|---|---|---|---|
| 累成狗 | 空 | 含两个正确 ID | 词法漏召回，靠另一条路补 |
| 下班 | 相关图首位 | 相关图第三位 | 候选来源与首屏来源不同 |
| 猫 | 正例首位 | 正例第二位 | 融合改善 MRR 而不是 Recall |
| 量子力学 | 单个字误召 | 手填一队错误项 | 无答案的错返需独立统计 |

再做[完整图解案例](../worked-example/README.md)的 X 可以反超 A 与 B 的例子。保存一份候选级表和一份展示级表，解释新增候选数、展示命中与过滤中丢失。如果想改融合，这里给两种可比较方案：

- **原始 RRF**，每路 1/(60+rank)，固定词法、图文各 L 条，最后展示 K。
- **两路首位保留**，先取两路的第一条，移除重复，再以 RRF 择剩余。对确切台词可以另做测试，但不要一次也改路内排行。

双方使用相同输入、相同候选上限和同样的展示 K，报告退化的案例。只在固定的四条用于演示的 query 获益，不足以验证策略在真实场景好。

## 12.4 里程碑 C：把手填视觉候选换成实际图片

### 先建立目录，不先跑模型

```text
data/private/
  manifest.json              每行对象的 ID、text、image
  images/
    one.png
    two.jpg
outputs/
  query-traces/              本地结果，不上传私有图片
  experiment.md              公开报告可删去具体图片内容
```

建议 10–30 张授权图先验收单图输入；可用明确区分的物体、姿势和情绪，另准备至少一条反义 query、两条无答案 query。把图中 OCR 与标签分栏保存，在建立词法输入时写清采用哪些字段。先标注与划分，再开始比较，不要只用你为了演示而挑的成功案例。

### 单图阶段：确认「像素真的被读取」

```bash
python scripts/clip_search.py --manifest data/private/manifest.json --query '困得睁不开眼' --device cpu --k 5
python scripts/clip_search.py --manifest data/private/manifest.json --query '困得睁不开眼' --device cpu --k 5 --hybrid
```

第一条只有图文路，第二条才加入词法融合。模型依赖、图片相对路径和默认 checkpoint 见 [第 06 章](../06-quickstart/README.md)。你应看到唯一图 ID、标签和路径；若失败，先单独读 manifest、检查文件，只有单图推理成功之后再批量。此脚本每条请求会重算图片向量，以教学为目的，不拿其延时当生产指标。

### 正式对照：样本量、K 和版本要落在结果旁边

保存自己实际得出的值。若某路未跑，写「未运行」，不要填预期数字。

| 策略 | 固定图库/标签版本 | Recall@K | MRR@K | 无答案错返 | 主要失败 |
|---|---|---:|---:|---:|---|
| BM25 | 填实测版本 |  |  |  |  |
| 图文 | 同上 |  |  |  |  |
| RRF | 同上 |  |  |  |  |
| 改一个融合条件 | 同上 |  |  |  |  |

## 12.5 交付检查与面试复盘

除了数字，附一次请求的完整路径，能展示 token、每路得分和名次、被移除的候选以及最终展示。写一条正例入不了图库的限制，另一条正确图进池却降序的案例；两者为什么需要不同的改动。若只完成 A 与 B，就将项目写为「中文图片检索管线与离线评测」，图文部分明确预接入或模拟，不写成真实模型训练。

<details>
<summary>复盘作业：面试官说“你加语义路提高了准确率”该如何更精确地说？</summary>

先说实际验证范围：手填视觉榜证明融合实现能接入独有正例，不证明 CLIP 真实表现；有实图实验之后，再说哪类 query 的候选覆盖改善、固定首屏 K 是否同步改善、额外延时是多少。保留失败案例，结论才能经得住追问。
</details>

---
[返回首页](../../README.md) · [上一章](../11-serving/README.md) · [下一章](../13-interview/README.md)

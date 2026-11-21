# 04 · 源码阅读：编码、检索、训练

## 跟一次真实调用：从字符串到指标

在仓库根目录运行：

```bash
python3 scripts/demo.py --query '疲惫'
```

先看两行输出：第一行是这次交互查询的结果，第二行是固定评测文件中全部查询的汇总。改命令行的 `--query` 只影响第一行。若想比较两种输入的总体效果，需要给 `--queries` 新的评测文件，而不是用一条查询的肉眼判断替代评测。

调用顺序是 [demo.py](../../scripts/demo.py) → [retrieval.py](../../scripts/retrieval.py) → [metrics.py](../../scripts/metrics.py)。加载 manifest 后，`BM25.__init__` 为每个条目构建词频表、文档长度和全库文档频率。注意文档频率统计遍历的是 Counter 的键：一张图描述里出现三个「累」，在 DF 里仍只算一个文档。查询时 `set(tokens(query))` 把重复字符折成一次贡献；文档侧的词频仍参与打分。结果按负分和 ID 排序，所以同分会用字典序固定下来。

可以在同一次解释器调用里检查所有中间值：

```bash
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "scripts")
from retrieval import BM25, tokens
docs = json.loads(Path("data/sample/memes.json").read_text())
model = BM25(docs)
print(tokens("疲惫"))
print("平均长度", model.avg, "文档频率", {k:model.df[k] for k in tokens("疲惫")})
print("排序", model.search("疲惫", 3))
PY
```

排查「为什么搜索结果为空」时，先打印规范化后的 token，再看这几个 token 在 DF 表里是否出现。比如纯标点会没有 token；若只有图像像素、没有任何文字描述，文字检索也自然没有这部分信号。最后才考虑调参数。如果能召回结果但排序奇怪，从每个候选的文档长度、命中的字符和同分规则查起。

## 改动代码时对齐输入输出

| 层 | 输入 | 输出 | 最容易踩的坑 |
|---|---|---|---|
| 分词 | 查询字符串或标签 | token 序列 | 只改查询端，建库端仍用旧分词 |
| 词法检索 | 查询、K、标签库 | ID 和分数 | 把 BM25 分数当概率 |
| 图文检索 | 路径、查询、模型 | 余弦分数排序 | 用 manifest 的旧行号映射新向量 |
| 融合 | 每一路的有序 ID | 合并后的唯一 ID | 提前截断或重复候选重复加分 |
| 评测 | ID 排名、正例集合、K | 四个指标或空值 | 没有正例和一个都没找到混成一类 |

图文入口 [clip_search.py](../../scripts/clip_search.py) 是可选脚本。它将图片转换成 RGB、利用模型的预处理变成单张图像批次，逐张取向量并归一化。文本经 tokenizer 和文本编码器之后同样归一化，再做一次矩阵乘法。它把所有图在每次调用中重编码，适合看懂全流程；服务化必须把编码与查询分离。GIF 暂按首帧处理，如果文字只在后半段出现，首帧没有机会提供这个信号。

练习：把两个文档的标签写成完全相同，再交换 manifest 中的顺序。预期两条分数相同，而且由于最终按 ID 字典序排序，前后顺序一致。若换成只按分数排序，同分就可能受到输入顺序影响。

先执行 [参考代码下载脚本](../../scripts/fetch_references.py)，再沿调用链阅读，避免从头到尾逐行背代码。

| 阅读顺序 | 文件 | 带着什么问题读 |
|---|---|---|
| 1 | StickerSearch `image_search_core/model_loader.py` | 模型何时加载？设备如何选？ |
| 2 | `image_search_core/indexer.py` | 文件变化如何发现？向量如何与路径对应？ |
| 3 | `image_search_core/searcher.py` | 文本如何编码？归一化在哪里做？Top K如何得到？ |
| 4 | Chinese-CLIP `cn_clip/clip/model.py` | 两个编码器如何投影到共同空间？ |
| 5 | `cn_clip/training/train.py` | 正例标签是什么？跨卡负样本如何聚合？ |

以上文件存在于 SOURCES 中固定的提交。不要依赖浮动的 main 行号。先用自己的话写函数的输入、输出、张量维度，再进入细节。

本仓库对应阅读：`scripts/retrieval.py` 的 `BM25.search` 是词法召回，`rrf` 是基于名次的融合；`scripts/clip_search.py` 是模型加载、图片编码、查询编码和归一化点积的最小链路。它没有微调训练器，也没有持久化 ANN 索引。

## 走读任务

假定 4 张图片、512 维向量、1 条查询，写出图片矩阵 `[4,512]`、查询矩阵 `[1,512]`、分数矩阵 `[1,4]`。修改 Top K 为超过图库大小，检查边界；然后解释空查询与未知词为何应该有确定行为。

---
[返回首页](../../README.md) · [上一章](../03-architecture/README.md) · [下一章](../05-clip-learning/README.md)

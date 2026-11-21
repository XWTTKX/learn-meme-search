# Learn Meme Search · 中文表情包搜索

**面向大厂搜广推算法面试的学习指南：从文字检索到多模态召回、融合与评测。**

可以从[逐步读代码](docs/04-source-walkthrough/README.md)入手，再做[BM25 与 RRF 手算](docs/08-lexical-hybrid/README.md)、[CLIP 双向损失推导](docs/05-clip-learning/README.md)和[离线评测](docs/10-evaluation/README.md)。运行 `python3 scripts/fusion_lab.py`，观察台词、语义、对象和无答案四类查询如何影响融合；实际输出与后续图文实验见[实战章](docs/12-project-labs/README.md)。

参考 [learn-nanobot](https://github.com/bcefghj/learn-nanobot) 的“分章节学习 → 源码走读 → 实战 → 面试”结构，重新编写领域内容。目标是做出能复现、能解释、能接受追问的个人项目。场景类似微信文字搜表情包，与微信官方实现无关联。

## 项目选择

主线：[Chinese-CLIP](https://github.com/OFA-Sys/Chinese-CLIP) + [StickerSearch](https://github.com/oftx/StickerSearch)；补充参考：[MEME-Indexer](https://github.com/VEWOXIC/MEME-Indexer)。选择依据、固定提交和许可说明见 [SOURCES.md](SOURCES.md)。

## 当前交付状态

| 内容 | 状态 |
|---|---|
| 中文17章教程、源码路线、面试与简历模板 | 已提供 |
| 标准库BM25、RRF、指标与示例数据 | 已运行测试 |
| Chinese-CLIP图文检索脚本 | 已提供；需用户图片及模型，未运行真实推理 |
| OCR、微调、Faiss服务与线上压测 | 教程扩展任务，尚未实现 |
| 真实图片benchmark/线上提升 | 未执行，无成果数字 |

## 四阶段路线

```mermaid
flowchart LR
  A[基础与源码 01-05] --> B[动手与评测 06-10]
  B --> C[工程与实战 11-12]
  C --> D[面试与表达 13-17]
```

## 章节目录

| 章节 | 阅读入口 |
|---|---|
| 01 | [搜索系统基础：从一句话到候选集](docs/01-search-basics/README.md) |
| 02 | [开源项目筛选与边界](docs/02-project-selection/README.md) |
| 03 | [端到端架构与数据流](docs/03-architecture/README.md) |
| 04 | [源码阅读：编码、检索、训练](docs/04-source-walkthrough/README.md) |
| 05 | [CLIP、InfoNCE与困难负样本](docs/05-clip-learning/README.md) |
| 06 | [安装与第一条查询](docs/06-quickstart/README.md) |
| 07 | [数据准备、标注与防泄漏](docs/07-data-labeling/README.md) |
| 08 | [OCR、BM25与RRF融合](docs/08-lexical-hybrid/README.md) |
| 09 | [精确检索、Faiss与索引更新](docs/09-vector-index/README.md) |
| 10 | [离线评测与bad case分析](docs/10-evaluation/README.md) |
| 11 | [服务化、延迟与可观测性](docs/11-serving/README.md) |
| 12 | [三阶段实战与六周安排](docs/12-project-labs/README.md) |
| 13 | [高频面试题与回答要点](docs/13-interview/README.md) |
| 14 | [对应搜广推岗位的能力](docs/14-role-mapping/README.md) |
| 15 | [简历写法与成果证据](docs/15-resume/README.md) |
| 16 | [90秒介绍与项目深挖](docs/16-star/README.md) |
| 17 | [资源与下一步阅读](docs/17-resources/README.md) |

## 五分钟开始

```bash
python3 scripts/demo.py --query '不想上班'
python3 -m unittest discover -s tests -v
```

无需GPU、第三方依赖或外部数据。示例是手写文字标签，结果只用于冒烟检查。接入真实图片见[第06章](docs/06-quickstart/README.md)。

```text
docs/          17章中文教程
projects/      三阶段实践说明
scripts/       检索、模型入口、评测与上游下载
data/sample/   原创文字示例
experiments/   验证记录、实验模板
tests/         指标与检索正确性测试
```

先读01–06，跑基线，再准备数据。推荐与另一个仓库 learn-note-recsys 配合，两个项目合计按六周路线推进。第一天的目标是能解释一条查询的整个数据流。

本仓库原创代码与文字采用[MIT许可](LICENSE)；引用的项目、模型与数据保留各自许可。未重新分发上游应用、权重或表情包。

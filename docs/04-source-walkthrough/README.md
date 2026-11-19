# 04 · 源码阅读：编码、检索、训练

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

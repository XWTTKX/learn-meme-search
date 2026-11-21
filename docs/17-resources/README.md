# 17 · 资源与下一步阅读

## 按问题查资料

先读 [CLIP](https://arxiv.org/abs/2103.00020) 的训练目标与零样本推理，再读 [Chinese-CLIP](https://arxiv.org/abs/2211.01335) 的中文训练背景。读完画出输入和投影后的两个矩阵，自己转置做双向交叉熵。论文指标通常来自特定数据和任务；表情包的短句、网络梗、OCR 与 GIF 不能直接套结论。练完模型再读 [Faiss 索引表](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)，自己用精确 TopK 定义 ANN Recall，而不是照搬别人的索引参数。

每次读源代码建议留下三行笔记：哪一层有输入输出接口、版本改动会破坏哪个假设、在自己的项目里如何验证。最后把论文、代码提交和测试数据版本记录在[来源表](../../SOURCES.md)与实验记录中。

优先阅读原始仓库和论文。版本化项目入口见 [SOURCES.md](../../SOURCES.md)。

- [Chinese-CLIP](https://github.com/OFA-Sys/Chinese-CLIP)：图文编码与训练实现。
- [CLIP论文](https://arxiv.org/abs/2103.00020)：理解双编码器对比学习。
- [Chinese CLIP论文](https://arxiv.org/abs/2211.01335)：理解中文数据与训练设置。
- [Faiss文档](https://github.com/facebookresearch/faiss/wiki)：向量检索及索引选择。
- [StickerSearch](https://github.com/oftx/StickerSearch)：索引与本地交互导读。
- [MEME-Indexer](https://github.com/VEWOXIC/MEME-Indexer)：移动端产品参考。

读论文只需先回答：问题是什么、目标函数是什么、训练样本如何构造、评测是否与自己的任务相符。不要把论文在公开benchmark上的结果当成表情包数据上的保证。

完成本仓库后转入笔记推荐项目，重点补用户历史、多路召回、特征交叉与多目标学习。两个项目共同形成从检索到推荐的能力链。

---
[返回首页](../../README.md) · [上一章](../16-star/README.md)

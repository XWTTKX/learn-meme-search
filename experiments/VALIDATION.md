# 本地验证记录

2026-11-21：重新运行 5 项单测、基础 demo 和 [fusion_lab.py](../scripts/fusion_lab.py)。四组融合案例跑通：语义查询中手填视觉榜贡献两个独有正例；台词查询中词法路把视觉榜第三的正例提到首位；无答案组仍可出现候选，但相关性指标返回 null。视觉榜为受控教学数据，没有用真实图片模型生成。

日期：2026-11-17；环境：macOS，Python 3.9.6，CPU；无第三方包。

执行：`python3 -m unittest discover -s tests -v`，5项测试通过。覆盖多正例Recall与HitRate区别、空正例、重复结果、理想NDCG、中文词法匹配与RRF去重。

执行：`python3 scripts/demo.py --query '不想上班'`，返回m01为首位。6条原创文字查询在8项文字样例上，K=3时Recall/MRR/NDCG均为1.0。这是人为构造的冒烟数据，完全不能表示真实图片检索质量。

已检查全部Python文件可编译、Markdown相对链接可解析。可选Chinese-CLIP脚本未安装模型依赖、未下载权重、未执行真实图片推理；仅语法检查。OCR、ANN、微调与服务压测尚未实现。

真实实验使用TEMPLATE.md单独记录，不用这份软件检查代替效果评测。

# 06 · 安装与第一条查询

## 无下载基线（Python 3.9+）

在仓库根目录执行：

```bash
python3 scripts/demo.py --query '不想上班'
python3 -m unittest discover -s tests -v
```

标准库基线只查手写文字标签，不读取图片。示例 manifest 中的图片路径是占位符，仓库不附带表情包。示例 6 条查询用于验证接口和公式，满分不能解释成真实检索效果。

## 可选图文推理（需要图片与模型下载）

建议单独创建 Python 3.10/3.11 环境，按设备安装相容的 PyTorch，再安装 `requirements-model.txt`。范围约束不是完整环境锁；跑通后执行 `pip freeze > experiments/model-environment.txt` 保存实际版本。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-model.txt
python scripts/clip_search.py --manifest data/private/manifest.json --query '不想上班' --device cpu --hybrid
```

manifest 是 JSON 数组，每项含 `id,text,image`。`image` 相对 manifest 所在目录；`text` 为人工描述或OCR文字。先用 10 张有使用权的图片验证。模型下载和真实图片推理未在交付环境执行，不能把命令存在当作复现完成。

排错顺序：确认 Python/torch 版本 → 模型能下载 → 图片路径可读 → 单图编码 → 再批量。CPU路径优先，CUDA需要兼容驱动；不要默认Mac支持CUDA。

---
[返回首页](../../README.md) · [上一章](../05-clip-learning/README.md) · [下一章](../07-data-labeling/README.md)

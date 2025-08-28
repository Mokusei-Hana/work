# 基于隐写技术的数字版权保护与检测系统

> 毕设仓库 · Python(FastAPI) · 可复现实验

## 功能
- 图像隐写：LSB（示例）+ DCT/DWT（待实现）
- 版权水印：作者/许可证信息嵌入与提取（占位签名）
- 检测：统计/ML 检测框架
- 评价：PSNR/SSIM/BER 等

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . -r requirements.txt
pytest
uvicorn src.server.main:app --reload --port 8000

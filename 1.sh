# 1) 基本文件
echo "# 基于隐写技术的数字版权保护与检测系统" > README.md
echo "MIT License" > LICENSE

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
.venv/
.env
dist/
build/
*.egg-info/
# Data
data/*.zip
data/*.tar*
data/samples/*
# IDE
.vscode/
.idea/
# OS
.DS_Store
EOF

# 2) Python项目 & 工具
cat > pyproject.toml << 'EOF'
[project]
name = "drmstego"
version = "0.1.0"
description = "Steganography-based Digital Rights Protection & Detection"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "fastapi",
  "uvicorn[standard]",
  "pillow",
  "numpy",
  "scipy",
  "scikit-image",
  "pydantic>=2",
  "typer",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
addopts = "-q"

[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E","F","I","UP","B"]
ignore = []

[tool.isort]
profile = "black"
EOF

cat > requirements.txt << 'EOF'
fastapi
uvicorn[standard]
pillow
numpy
scipy
scikit-image
pydantic>=2
typer
EOF

cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks: [{id: black}]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks: [{id: ruff}]
EOF

# 3) CI
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e . -r requirements.txt
      - run: pip install pytest
      - run: pytest
EOF

# 4) 目录
mkdir -p docs data/samples src/drmstego/{steg,detect,drm} src/server tests
echo "示例数据说明；大文件请勿入库。" > data/README.md
echo "待写：项目总览与术语。" > docs/00_overview.md
echo "待写：系统设计图与模块说明。" > docs/01_design.md
echo "待写：算法实现细节与对比实验。" > docs/02_algorithms.md
echo "待写：API说明与示例。" > docs/03_api.md
echo "随手记录实验与想法。" > docs/99_notes.md

# 5) Python包骨架
cat > src/drmstego/__init__.py << 'EOF'
__all__ = ["steg", "detect", "metrics", "drm"]
EOF

cat > src/drmstego/steg/base.py << 'EOF'
from abc import ABC, abstractmethod
from typing import Any

class StegoAlgorithm(ABC):
    """隐写算法抽象基类"""

    @abstractmethod
    def embed(self, cover: Any, payload: bytes, **kwargs) -> Any:
        """将payload嵌入到cover中，返回stego对象"""
        raise NotImplementedError

    @abstractmethod
    def extract(self, stego: Any, **kwargs) -> bytes:
        """从stego对象中提取payload"""
        raise NotImplementedError
EOF

cat > src/drmstego/steg/lsb.py << 'EOF'
from PIL import Image
import numpy as np
from .base import StegoAlgorithm

class LSBStego(StegoAlgorithm):
    """简单LSB图像隐写（演示用，非生产）"""

    def embed(self, cover, payload: bytes, *, channel: int = 0) -> Image.Image:
        img = cover.convert("RGB")
        arr = np.array(img)
        bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
        h, w, _ = arr.shape
        capacity = h * w
        if bits.size > capacity:
            raise ValueError(f"载荷过大：{bits.size}bits > 容量{capacity}bits")
        flat = arr[:, :, channel].flatten()
        flat[: bits.size] = (flat[: bits.size] & ~1) | bits
        arr[:, :, channel] = flat.reshape(h, w)
        return Image.fromarray(arr)

    def extract(self, stego, *, length_bytes: int, channel: int = 0) -> bytes:
        img = stego.convert("RGB")
        arr = np.array(img)
        h, w, _ = arr.shape
        bits_need = length_bytes * 8
        flat = arr[:, :, channel].flatten()
        bits = flat[:bits_need] & 1
        return np.packbits(bits).tobytes()
EOF

cat > src/drmstego/steg/dct.py << 'EOF'
# DCT频域隐写骨架：后续可在8x8块上修改系数
from .base import StegoAlgorithm

class DCTStego(StegoAlgorithm):
    def embed(self, cover, payload: bytes, **kwargs):
        raise NotImplementedError("TODO: 实现DCT频域嵌入")

    def extract(self, stego, **kwargs) -> bytes:
        raise NotImplementedError("TODO: 实现DCT频域提取")
EOF

cat > src/drmstego/steg/dwt.py << 'EOF'
# DWT小波域隐写骨架
from .base import StegoAlgorithm

class DWTStego(StegoAlgorithm):
    def embed(self, cover, payload: bytes, **kwargs):
        raise NotImplementedError("TODO: 实现DWT域嵌入")

    def extract(self, stego, **kwargs) -> bytes:
        raise NotImplementedError("TODO: 实现DWT域提取")
EOF

cat > src/drmstego/io_utils.py << 'EOF'
from hashlib import sha256
from pathlib import Path
from typing import Tuple
from PIL import Image

def read_image(path: str | Path) -> Image.Image:
    return Image.open(path).convert("RGB")

def save_image(img: Image.Image, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    img.save(path)

def file_sha256(path: str | Path) -> str:
    data = Path(path).read_bytes()
    return sha256(data).hexdigest()

def bytes_sha256(b: bytes) -> str:
    return sha256(b).hexdigest()
EOF

cat > src/drmstego/metrics.py << 'EOF'
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def psnr_rgb(a, b) -> float:
    return psnr(np.array(a), np.array(b), data_range=255)

def ssim_rgb(a, b) -> float:
    return ssim(np.array(a), np.array(b), channel_axis=2, data_range=255)
EOF

cat > src/drmstego/drm/watermark.py << 'EOF'
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class WatermarkPayload:
    author: str
    license_id: str
    issued_at: str
    extra: dict

    def to_bytes(self) -> bytes:
        return json.dumps({
            "author": self.author,
            "license_id": self.license_id,
            "issued_at": self.issued_at,
            "extra": self.extra,
        }, ensure_ascii=False).encode("utf-8")

def make_simple_watermark(author: str, license_id: str, **extra) -> bytes:
    wm = WatermarkPayload(author=author, license_id=license_id,
                          issued_at=datetime.utcnow().isoformat()+"Z",
                          extra=extra)
    return wm.to_bytes()
EOF

cat > src/drmstego/drm/license_token.py << 'EOF'
# 轻量级占位：后续可用非对称签名（Ed25519）做许可证防伪
def sign_token(payload: bytes) -> bytes:
    return payload  # TODO: 替换为真实签名

def verify_token(token: bytes) -> bool:
    return True     # TODO: 校验签名
EOF

cat > src/drmstego/detect/classical.py << 'EOF'
# 占位：添加RS分析、卡方检测、噪声残差统计等
def chi_square_detect(image) -> float:
    """返回可疑度分数（越高越可疑）"""
    return 0.0
EOF

cat > src/drmstego/detect/ml.py << 'EOF'
# 预留：特征提取+分类器/轻量CNN
class SimpleStegoDetector:
    def predict(self, image) -> float:
        return 0.0
EOF

cat > src/drmstego/cli.py << 'EOF'
import typer
from pathlib import Path
from PIL import Image
from .steg.lsb import LSBStego
from .io_utils import read_image, save_image
from .drm.watermark import make_simple_watermark

app = typer.Typer(help="隐写-版权 研究用 CLI")

@app.command()
def embed(cover: str, out: str, text: str):
    """将文本水印嵌入到图像(LSB示例)"""
    img = read_image(cover)
    payload = text.encode("utf-8")
    stego = LSBStego().embed(img, payload)
    save_image(stego, out)
    typer.echo(f"已保存：{out}")

@app.command()
def extract(stego: str, length: int):
    """从图像中提取固定长度字节"""
    img = read_image(stego)
    data = LSBStego().extract(img, length_bytes=length)
    typer.echo(data.decode("utf-8", errors="ignore"))

@app.command()
def embed_license(cover: str, out: str, author: str, license_id: str):
    """将简单许可证信息作为水印写入"""
    img = read_image(cover)
    payload = make_simple_watermark(author, license_id)
    stego = LSBStego().embed(img, payload)
    save_image(stego, out)
    typer.echo(f"写入license水印完成：{out}（长度 {len(payload)} 字节）")

if __name__ == "__main__":
    app()
EOF

# 6) API服务
cat > src/server/schemas.py << 'EOF'
from pydantic import BaseModel

class EmbedRequest(BaseModel):
    text: str

class ExtractRequest(BaseModel):
    length: int
EOF

cat > src/server/main.py << 'EOF'
from fastapi import FastAPI, UploadFile
from PIL import Image
from io import BytesIO
from drmstego.steg.lsb import LSBStego

from .schemas import EmbedRequest, ExtractRequest

app = FastAPI(title="DRM Stego API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/embed")
async def embed(img: UploadFile, req: EmbedRequest):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    stego = LSBStego().embed(image, req.text.encode("utf-8"))
    buf = BytesIO()
    stego.save(buf, format="PNG")
    buf.seek(0)
    return {"image_bytes": list(buf.getvalue()), "length": len(req.text.encode('utf-8'))}

@app.post("/extract")
async def extract(img: UploadFile, req: ExtractRequest):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    data = LSBStego().extract(image, length_bytes=req.length)
    return {"text": data.decode("utf-8", errors="ignore")}
EOF

# 7) 测试
cat > tests/test_lsb.py << 'EOF'
from PIL import Image
from drmstego.steg.lsb import LSBStego

def test_lsb_roundtrip():
    img = Image.new("RGB", (64, 64), color=(123, 222, 111))
    msg = b"hello stego"
    stego = LSBStego().embed(img, msg)
    out = LSBStego().extract(stego, length_bytes=len(msg))
    assert out == msg
EOF

cat > tests/test_metrics.py << 'EOF'
from PIL import Image
from drmstego.metrics import psnr_rgb
def test_psnr_basic():
    a = Image.new("RGB", (16,16), color=(0,0,0))
    b = Image.new("RGB", (16,16), color=(1,1,1))
    assert psnr_rgb(a,b) > 40
EOF

cat > tests/test_api.py << 'EOF'
from fastapi.testclient import TestClient
from src.server.main import app
from PIL import Image
from io import BytesIO

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.json()["ok"] is True

def test_embed_extract():
    img = Image.new("RGB", (64,64), color=(100,100,100))
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    r = client.post("/embed", files={"img": ("a.png", buf.getvalue(), "image/png")},
                    json={"text":"abc"})
    assert r.status_code == 200
EOF

# 8) 安全说明
cat > SECURITY.md << 'EOF'
- 不要将含个人信息或受版权保护的大文件直接入库。
- 对第三方数据集标注来源与许可证。
- 研究代码默认仅用于学术与教学，生产前需进行安全评估与审计。
EOF

git add .
git commit -m "chore: 初始化项目框架"

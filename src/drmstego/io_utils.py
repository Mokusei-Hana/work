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

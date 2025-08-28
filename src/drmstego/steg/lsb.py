import numpy as np
from PIL import Image

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
        flat[: bits.size] = (flat[: bits.size] & np.uint8(0xFE)) | bits
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

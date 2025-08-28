"""离散小波变换(DWT)隐写实现.

该实现仅用于演示, 将载荷的比特嵌入某一小波子带系数的最低有效位。
默认在第一层分解的 ``HH`` 子带中嵌入, 可以通过参数调整小波类型、
分解层级以及使用的子带。
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pywt
from PIL import Image

from .base import StegoAlgorithm


class DWTStego(StegoAlgorithm):
    """基于二维离散小波变换的简单隐写"""

    def embed(
        self,
        cover,
        payload: bytes,
        *,
        channel: int = 0,
        wavelet: str = "haar",
        level: int = 1,
        embed_level: int | None = None,
        subband: Literal["LH", "HL", "HH"] = "HH",
    ) -> Image.Image:
        """将载荷嵌入 ``cover`` 图像.

        Parameters
        ----------
        cover: PIL.Image.Image
            载体图像
        payload: bytes
            待嵌入数据
        channel: int, optional
            对 RGB 图像的哪个通道进行嵌入, 默认第一个通道
        wavelet: str, optional
            小波类型, 默认为 ``haar``
        level: int, optional
            DWT 分解层级, 默认 1
        embed_level: int, optional
            使用哪个层级的系数进行嵌入, ``1`` 表示最细节层(默认)
        subband: {"LH", "HL", "HH"}
            选择的子带
        """

        if embed_level is None:
            embed_level = 1

        img = cover.convert("RGB")
        arr = np.array(img, dtype=np.float32)

        bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))

        coeffs = pywt.wavedec2(arr[:, :, channel], wavelet=wavelet, level=level)
        cA, *details = coeffs
        target = list(details[-embed_level])

        band_map = {"LH": 0, "HL": 1, "HH": 2}
        band_idx = band_map[subband]
        band = target[band_idx]

        flat = np.round(band).astype(np.int32).flatten()
        capacity = flat.size
        if bits.size > capacity:
            raise ValueError(f"载荷过大：{bits.size}bits > 容量{capacity}bits")

        flat[: bits.size] = (flat[: bits.size] & ~1) | bits
        target[band_idx] = flat.reshape(band.shape).astype(np.float32)

        details[-embed_level] = tuple(target)
        coeffs_mod = [cA] + details

        channel_arr = pywt.waverec2(coeffs_mod, wavelet)
        channel_arr = np.clip(channel_arr, 0, 255)
        arr[:, :, channel] = channel_arr[: arr.shape[0], : arr.shape[1]]

        return Image.fromarray(arr.astype(np.uint8))

    def extract(
        self,
        stego,
        *,
        length_bytes: int,
        channel: int = 0,
        wavelet: str = "haar",
        level: int = 1,
        embed_level: int | None = None,
        subband: Literal["LH", "HL", "HH"] = "HH",
    ) -> bytes:
        """从 ``stego`` 图像中提取载荷."""

        if embed_level is None:
            embed_level = 1

        img = stego.convert("RGB")
        arr = np.array(img, dtype=np.float32)

        coeffs = pywt.wavedec2(arr[:, :, channel], wavelet=wavelet, level=level)
        _, *details = coeffs
        target = details[-embed_level]

        band_map = {"LH": 0, "HL": 1, "HH": 2}
        band_idx = band_map[subband]
        band = target[band_idx]

        flat = np.round(band).astype(np.int32).flatten()
        bits_need = length_bytes * 8
        bits = flat[:bits_need] & 1
        return np.packbits(bits).tobytes()

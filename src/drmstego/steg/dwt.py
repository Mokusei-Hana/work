# DWT小波域隐写骨架
from .base import StegoAlgorithm

class DWTStego(StegoAlgorithm):
    def embed(self, cover, payload: bytes, **kwargs):
        raise NotImplementedError("TODO: 实现DWT域嵌入")

    def extract(self, stego, **kwargs) -> bytes:
        raise NotImplementedError("TODO: 实现DWT域提取")

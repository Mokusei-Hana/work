# DCT频域隐写骨架：后续可在8x8块上修改系数
from .base import StegoAlgorithm

class DCTStego(StegoAlgorithm):
    def embed(self, cover, payload: bytes, **kwargs):
        raise NotImplementedError("TODO: 实现DCT频域嵌入")

    def extract(self, stego, **kwargs) -> bytes:
        raise NotImplementedError("TODO: 实现DCT频域提取")

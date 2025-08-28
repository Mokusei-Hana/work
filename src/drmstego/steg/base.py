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

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

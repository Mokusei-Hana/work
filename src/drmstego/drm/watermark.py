import json
from dataclasses import dataclass
from datetime import datetime


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

    @classmethod
    def from_bytes(cls, data: bytes) -> "WatermarkPayload":
        try:
            obj = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise ValueError("Invalid watermark payload") from e
        if not isinstance(obj, dict):
            raise ValueError("Invalid watermark payload")
        try:
            author = obj["author"]
            license_id = obj["license_id"]
            issued_at = obj["issued_at"]
            extra = obj.get("extra", {})
        except KeyError as e:
            raise ValueError("Missing field in watermark payload") from e
        if not isinstance(extra, dict):
            raise ValueError("Invalid watermark payload")
        return cls(author=author, license_id=license_id, issued_at=issued_at, extra=extra)

def make_simple_watermark(author: str, license_id: str, **extra) -> bytes:
    wm = WatermarkPayload(
        author=author,
        license_id=license_id,
        issued_at=datetime.utcnow().isoformat() + "Z",
        extra=extra,
    )
    return wm.to_bytes()

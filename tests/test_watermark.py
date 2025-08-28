import pytest

from drmstego.drm.watermark import WatermarkPayload


def test_watermark_roundtrip():
    wm = WatermarkPayload(
        author="Alice",
        license_id="LIC123",
        issued_at="2023-01-01Z",
        extra={"note": "hi"},
    )
    data = wm.to_bytes()
    parsed = WatermarkPayload.from_bytes(data)
    assert parsed == wm

def test_watermark_invalid_bytes():
    with pytest.raises(ValueError):
        WatermarkPayload.from_bytes(b"not-json")

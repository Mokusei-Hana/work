from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from drmstego.drm.watermark import make_simple_watermark
from drmstego.steg.lsb import LSBStego
from server.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.json()["ok"] is True

def test_embed_extract():
    img = Image.new("RGB", (64, 64), color=(100, 100, 100))
    payload = make_simple_watermark("Alice", "L1")
    stego = LSBStego().embed(img, payload)
    buf = BytesIO()
    stego.save(buf, format="PNG")
    buf.seek(0)
    r = client.post(
        "/extract",
        files={"img": ("a.png", buf.getvalue(), "image/png")},
        data={"length": len(payload)},
    )
    assert r.status_code == 200
    assert r.json()["watermark"]["author"] == "Alice"

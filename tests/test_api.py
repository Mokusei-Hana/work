from fastapi.testclient import TestClient
from src.server.main import app
from PIL import Image
from io import BytesIO

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.json()["ok"] is True

def test_embed_extract():
    img = Image.new("RGB", (64,64), color=(100,100,100))
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    r = client.post("/embed", files={"img": ("a.png", buf.getvalue(), "image/png")},
                    json={"text":"abc"})
    assert r.status_code == 200

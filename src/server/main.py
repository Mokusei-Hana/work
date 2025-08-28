from io import BytesIO

from fastapi import FastAPI, Form, UploadFile
from PIL import Image

from drmstego.drm.watermark import WatermarkPayload
from drmstego.steg.lsb import LSBStego

from .schemas import EmbedRequest

app = FastAPI(title="DRM Stego API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/embed")
async def embed(img: UploadFile, req: EmbedRequest):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    stego = LSBStego().embed(image, req.text.encode("utf-8"))
    buf = BytesIO()
    stego.save(buf, format="PNG")
    buf.seek(0)
    return {"image_bytes": list(buf.getvalue()), "length": len(req.text.encode('utf-8'))}

@app.post("/extract")
async def extract(img: UploadFile, length: int = Form(...)):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    data = LSBStego().extract(image, length_bytes=length)
    try:
        wm = WatermarkPayload.from_bytes(data)
        return {"watermark": wm.__dict__}
    except ValueError:
        return {"text": data.decode("utf-8", errors="ignore")}

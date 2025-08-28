from fastapi import FastAPI, UploadFile
from PIL import Image
from io import BytesIO
from drmstego.steg.lsb import LSBStego

from .schemas import EmbedRequest, ExtractRequest

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
async def extract(img: UploadFile, req: ExtractRequest):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    data = LSBStego().extract(image, length_bytes=req.length)
    return {"text": data.decode("utf-8", errors="ignore")}

from fastapi import FastAPI, UploadFile, Form
from PIL import Image
from io import BytesIO
from drmstego.steg.lsb import LSBStego
from drmstego.drm.license_token import (
    sign_token as sign_token_bytes,
    verify_token as verify_token_bytes,
    SIGNATURE_LEN,
)

from .schemas import ExtractRequest, SignRequest, VerifyRequest

app = FastAPI(title="DRM Stego API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/embed")
async def embed(img: UploadFile, text: str = Form(...)):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    stego = LSBStego().embed(image, text.encode("utf-8"))
    buf = BytesIO()
    stego.save(buf, format="PNG")
    buf.seek(0)
    return {"image_bytes": list(buf.getvalue()), "length": len(text.encode('utf-8'))}

@app.post("/extract")
async def extract(img: UploadFile, req: ExtractRequest):
    image = Image.open(BytesIO(await img.read())).convert("RGB")
    data = LSBStego().extract(image, length_bytes=req.length)
    return {"text": data.decode("utf-8", errors="ignore")}


@app.post("/sign")
async def sign(req: SignRequest):
    token = sign_token_bytes(req.payload.encode("utf-8"))
    return {"token_hex": token.hex()}


@app.post("/verify")
async def verify(req: VerifyRequest):
    token = bytes.fromhex(req.token_hex)
    valid = verify_token_bytes(token)
    payload = (
        token[:-SIGNATURE_LEN].decode("utf-8", errors="ignore") if valid else None
    )
    return {"valid": valid, "payload": payload}

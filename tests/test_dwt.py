from PIL import Image

from drmstego.steg.dwt import DWTStego


def test_dwt_roundtrip():
    img = Image.new("RGB", (64, 64), color=(120, 200, 80))
    msg = b"wavelet stego"
    stego = DWTStego().embed(img, msg, wavelet="haar", level=2, subband="HH")
    out = DWTStego().extract(stego, length_bytes=len(msg), wavelet="haar", level=2, subband="HH")
    assert out == msg

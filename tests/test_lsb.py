from PIL import Image

from drmstego.steg.lsb import LSBStego


def test_lsb_roundtrip():
    img = Image.new("RGB", (64, 64), color=(123, 222, 111))
    msg = b"hello stego"
    stego = LSBStego().embed(img, msg)
    out = LSBStego().extract(stego, length_bytes=len(msg))
    assert out == msg

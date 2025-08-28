from PIL import Image
from drmstego.metrics import psnr_rgb
def test_psnr_basic():
    a = Image.new("RGB", (16,16), color=(0,0,0))
    b = Image.new("RGB", (16,16), color=(1,1,1))
    assert psnr_rgb(a,b) > 40

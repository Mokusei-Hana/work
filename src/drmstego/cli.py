import typer
from pathlib import Path
from PIL import Image
from .steg.lsb import LSBStego
from .io_utils import read_image, save_image
from .drm.watermark import make_simple_watermark
from .drm.license_token import (
    sign_token as sign_token_bytes,
    verify_token as verify_token_bytes,
    SIGNATURE_LEN,
)

app = typer.Typer(help="隐写-版权 研究用 CLI")

@app.command()
def embed(cover: str, out: str, text: str):
    """将文本水印嵌入到图像(LSB示例)"""
    img = read_image(cover)
    payload = text.encode("utf-8")
    stego = LSBStego().embed(img, payload)
    save_image(stego, out)
    typer.echo(f"已保存：{out}")

@app.command()
def extract(stego: str, length: int):
    """从图像中提取固定长度字节"""
    img = read_image(stego)
    data = LSBStego().extract(img, length_bytes=length)
    typer.echo(data.decode("utf-8", errors="ignore"))

@app.command()
def embed_license(cover: str, out: str, author: str, license_id: str):
    """将简单许可证信息作为水印写入"""
    img = read_image(cover)
    payload = make_simple_watermark(author, license_id)
    stego = LSBStego().embed(img, payload)
    save_image(stego, out)
    typer.echo(f"写入license水印完成：{out}（长度 {len(payload)} 字节）")


@app.command("sign-token")
def sign_token_cli(payload: str):
    """对payload进行签名并输出token(hex)"""

    token = sign_token_bytes(payload.encode("utf-8"))
    typer.echo(token.hex())


@app.command("verify-token")
def verify_token_cli(token_hex: str):
    """验证token并显示payload"""

    token = bytes.fromhex(token_hex)
    if verify_token_bytes(token):
        payload = token[:-SIGNATURE_LEN].decode("utf-8", errors="ignore")
        typer.echo(f"有效签名: {payload}")
    else:
        typer.echo("签名无效")

if __name__ == "__main__":
    app()

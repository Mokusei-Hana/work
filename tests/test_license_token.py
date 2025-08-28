from drmstego.drm.license_token import sign_token, verify_token, SIGNATURE_LEN
from drmstego.cli import app as cli_app
from typer.testing import CliRunner
from fastapi.testclient import TestClient
from src.server.main import app as api_app


def test_sign_verify_functions():
    payload = b"hello"
    token = sign_token(payload)
    assert verify_token(token)
    assert token[:-SIGNATURE_LEN] == payload
    tampered = bytearray(token)
    tampered[0] ^= 0x01
    assert not verify_token(bytes(tampered))


def test_cli_sign_verify():
    runner = CliRunner()
    res = runner.invoke(cli_app, ["sign-token", "hello"])
    assert res.exit_code == 0
    token_hex = res.stdout.strip()
    res2 = runner.invoke(cli_app, ["verify-token", token_hex])
    assert "有效签名" in res2.stdout
    assert "hello" in res2.stdout


def test_api_sign_verify():
    client = TestClient(api_app)
    r = client.post("/sign", json={"payload": "hello"})
    assert r.status_code == 200
    token_hex = r.json()["token_hex"]
    r2 = client.post("/verify", json={"token_hex": token_hex})
    assert r2.status_code == 200
    data = r2.json()
    assert data["valid"] is True
    assert data["payload"] == "hello"

# 轻量级占位：后续可用非对称签名（Ed25519）做许可证防伪
def sign_token(payload: bytes) -> bytes:
    return payload  # TODO: 替换为真实签名

def verify_token(token: bytes) -> bool:
    return True     # TODO: 校验签名

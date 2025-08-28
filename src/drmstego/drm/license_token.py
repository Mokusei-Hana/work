# 轻量级占位：后续可用非对称签名（Ed25519）做许可证防伪
"""License token helpers using Ed25519 signatures.

Token structure: ``payload || signature`` where signature is 64 bytes.
"""

from __future__ import annotations

import hashlib
from nacl.signing import SigningKey
from nacl.exceptions import BadSignatureError

# Ed25519 signature length in bytes
SIGNATURE_LEN = 64

# 使用固定seed以便测试和多进程稳定
_seed = hashlib.sha256(b"drmstego-ed25519-secret").digest()
_signing_key = SigningKey(_seed)
_verify_key = _signing_key.verify_key


def sign_token(payload: bytes) -> bytes:
    """Return ``payload`` appended with an Ed25519 signature."""

    signature = _signing_key.sign(payload).signature
    return payload + signature


def verify_token(token: bytes) -> bool:
    """Verify token consisting of ``payload || signature``.

    Returns ``True`` when the signature is valid, otherwise ``False``.
    """

    if len(token) <= SIGNATURE_LEN:
        return False
    payload, sig = token[:-SIGNATURE_LEN], token[-SIGNATURE_LEN:]
    try:
        _verify_key.verify(payload, sig)
        return True
    except BadSignatureError:
        return False


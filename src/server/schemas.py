from pydantic import BaseModel

class ExtractRequest(BaseModel):
    length: int


class SignRequest(BaseModel):
    payload: str


class VerifyRequest(BaseModel):
    token_hex: str

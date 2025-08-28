from pydantic import BaseModel

class EmbedRequest(BaseModel):
    text: str

class ExtractRequest(BaseModel):
    length: int

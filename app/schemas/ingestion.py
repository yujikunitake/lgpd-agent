from pydantic import BaseModel


class DocumentChunk(BaseModel):
    content: str
    metadata: dict

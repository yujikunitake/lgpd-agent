from pydantic import BaseModel


class QAResponse(BaseModel):
    answer: str
    sources: list[str]

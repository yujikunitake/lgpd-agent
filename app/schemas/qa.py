from pydantic import BaseModel, Field


class QAResponse(BaseModel):
    """Response schema containing the final answer and its source chunks."""

    answer: str = Field(description="The generated answer from the LLM.")
    sources: list[str] = Field(
        description="A list of source documents used to generate the answer."
    )

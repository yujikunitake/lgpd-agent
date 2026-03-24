from pydantic import BaseModel, Field

from app.schemas.agent import AgentStrategy


class Source(BaseModel):
    """Metadata about a source chunk used in the answer."""

    content: str
    location: str


class QAResponse(BaseModel):
    """Response schema containing the final answer, strategy, and source chunks."""

    answer: str = Field(description="The generated answer from the LLM.")
    strategy: AgentStrategy = Field(description="The strategy used by the agent.")
    sources: list[Source] = Field(
        description="A list of source documents used to generate the answer."
    )

from typing import Any

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """Structured representation of a processed text chunk of the LGPD."""

    content: str = Field(description="The text content of the chunk.")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata preserved from the markdown headers (e.g., Chapter, Article).",
    )

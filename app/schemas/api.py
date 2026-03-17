from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class AskRequest(BaseModel):
    """Schema for the incoming question request."""

    question: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
        Field(description="The question to be answered by the QA agent."),
    ]

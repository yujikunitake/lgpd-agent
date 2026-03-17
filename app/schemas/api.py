from typing import Annotated

from pydantic import BaseModel, StringConstraints


class AskRequest(BaseModel):
    question: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

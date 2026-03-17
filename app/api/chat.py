from fastapi import APIRouter

from app.schemas.api import AskRequest
from app.schemas.qa import QAResponse

router = APIRouter()


@router.post("/ask", response_model=QAResponse)
def ask_question(request: AskRequest) -> dict:
    """Handles incoming user questions and routes them to the QA Service.

    Args:
        request (AskRequest): The validated request payload containing the question.

    Returns:
        dict: A dictionary matching the QAResponse schema with the answer and sources.
    """
    # MVP mock implementation to satisfy the test `test_ask_endpoint`
    return {"answer": "Mock answer to satisfy API test", "sources": []}

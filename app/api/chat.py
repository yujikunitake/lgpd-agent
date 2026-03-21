from fastapi import APIRouter, Depends

from app.api.deps import get_qa_service
from app.schemas.api import AskRequest
from app.schemas.qa import QAResponse
from app.services.qa_service import QAService

router = APIRouter()


@router.post("/ask", response_model=QAResponse)
def ask_question(
    request: AskRequest, qa_service: QAService = Depends(get_qa_service)
) -> QAResponse:
    """Handles incoming user questions and routes them to the QA Service.

    Args:
        request (AskRequest): The validated request payload containing the question.

    Returns:
        QAResponse: A structured response containing the answer and sources.
    """

    return qa_service.ask(request.question)

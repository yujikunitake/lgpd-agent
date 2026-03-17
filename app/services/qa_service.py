from app.interfaces.qa_interfaces import LLMProtocol, RAGProtocol
from app.schemas.qa import QAResponse


class QAService:
    def __init__(self, llm: LLMProtocol, rag: RAGProtocol):
        self.llm = llm
        self.rag = rag

    def ask(self, question: str) -> QAResponse:
        sources = self.rag.retrieve(question)
        answer = self.llm.generate(prompt=question)

        return QAResponse(answer=answer, sources=sources)

from app.interfaces.qa_interfaces import LLMProtocol, RAGProtocol
from app.schemas.agent import AgentStrategy
from app.schemas.qa import QAResponse
from app.services.agent import Agent


class QAService:
    def __init__(self, llm: LLMProtocol, rag: RAGProtocol, agent: Agent):
        self.llm = llm
        self.rag = rag
        self.agent = agent

    def ask(self, question: str) -> QAResponse:
        strategy = self.agent.decide(question)

        sources = []
        if strategy == AgentStrategy.RAG:
            sources = self.rag.retrieve(question)

        answer = self.llm.generate(prompt=question)

        return QAResponse(answer=answer, sources=sources)

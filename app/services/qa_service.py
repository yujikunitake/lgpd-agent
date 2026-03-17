from app.interfaces.qa_interfaces import LLMProtocol, RAGProtocol
from app.schemas.agent import AgentStrategy
from app.schemas.qa import QAResponse
from app.services.agent import Agent


class QAService:
    """Service responsible for orchestrating the Question Answering flow."""

    def __init__(self, llm: LLMProtocol, rag: RAGProtocol, agent: Agent):
        """Initializes the QAService with its necessary dependencies.

        Args:
            llm (LLMProtocol): The language model text generator.
            rag (RAGProtocol): The document retriever for the knowledge base.
            agent (Agent): The agent responsible for strategy routing.
        """
        self.llm = llm
        self.rag = rag
        self.agent = agent

    def ask(self, question: str) -> QAResponse:
        """Processes a user question, potentially consulting RAG, and generates an answer.

        Args:
            question (str): The user's input question.

        Returns:
            QAResponse: The structured response containing the answer and its sources.
        """
        strategy = self.agent.decide(question)

        sources: list[str] = []
        if strategy == AgentStrategy.RAG:
            sources = self.rag.retrieve(question)

        answer = self.llm.generate(prompt=question)

        return QAResponse(answer=answer, sources=sources)

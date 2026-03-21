from app.services.agent import Agent
from app.services.embeddings import EmbeddingsService
from app.services.qa_service import QAService
from app.services.vector_rag_service import VectorRAGService
from app.services.vector_store import VectorStoreService

embeddings_service = EmbeddingsService()
vector_store_service = VectorStoreService()
vector_rag_service = VectorRAGService(embeddings_service, vector_store_service)


class MockLLM:
    def generate(self, prompt: str) -> str:
        return f"Resposta simulada para: {prompt}"


def get_qa_service() -> QAService:
    agent = Agent()
    llm = MockLLM()

    return QAService(llm, vector_rag_service, agent)

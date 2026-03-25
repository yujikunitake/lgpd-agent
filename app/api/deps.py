from app.database import engine
from app.services.agent import Agent
from app.services.embeddings import EmbeddingsService
from app.services.llm import LLMService
from app.services.qa_service import QAService
from app.services.vector_rag_service import VectorRAGService
from app.services.vector_store import VectorStoreService

embeddings_service = EmbeddingsService()
vector_store_service = VectorStoreService(engine)
vector_rag_service = VectorRAGService(embeddings_service, vector_store_service)
llm_service = LLMService(model="llama3.2:1b")


def get_qa_service() -> QAService:
    agent = Agent(embeddings_service)
    return QAService(llm_service, vector_rag_service, agent)

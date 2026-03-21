from app.interfaces.qa_interfaces import EmbeddingsProtocol, RAGProtocol
from app.services.vector_store import VectorStoreService


class VectorRAGService(RAGProtocol):
    """Implementation of RAG that uses vector search in PostgreSQL."""

    def __init__(
        self, embeddings_service: EmbeddingsProtocol, vector_store_service: VectorStoreService
    ):
        """Initializes the VectorRAGService.

        Args:
            embeddings_service (EmbeddingsProtocol): Service to generate embeddings from text.
            vector_store_service (VectorStoreService): Service to handle vector search.
        """
        self._embeddings_service = embeddings_service
        self._vector_store_service = vector_store_service

    def retrieve(self, question: str) -> list[str]:
        """Retrieves relevant document chunks from the vector store.

        Args:
            question (str): The user's query or question.

        Returns:
            list[str]: A list of text chunks retrieved based on vector similarity.
        """

        question_vector = self._embeddings_service.get_embedding(question)
        results = self._vector_store_service.search(question_vector, top_k=3)

        return [result["content"] for result in results]

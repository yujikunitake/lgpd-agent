import numpy as np

from app.schemas.agent import AgentStrategy
from app.services.embeddings import EmbeddingsService


class Agent:
    """Agent responsible for deciding the processing strategy for a user question."""

    def __init__(self, embeddings_service: EmbeddingsService, rag_threshold: int = 50):
        """Initializes the Agent.

        Args:
            embeddings_service (EmbeddingsService): Service for semantic similarity.
            rag_threshold (int): The character length threshold for RAG. Defaults to 50.
        """
        self.embeddings_service = embeddings_service
        self.rag_threshold = rag_threshold

        # Canonical greetings for semantic matching
        self.greetings = ["Olá", "Oi", "Bom dia", "Tudo bem?", "Quem é você?"]
        self._greeting_vectors = None

    def _get_greeting_vectors(self):
        """Lazy load greeting vectors."""
        if self._greeting_vectors is None:
            self._greeting_vectors = [
                np.array(self.embeddings_service.get_embedding(g)) for g in self.greetings
            ]
        return self._greeting_vectors

    @staticmethod
    def _cosine_similarity(v1, v2):
        """Simple cosine similarity between two normalized vectors."""
        return np.dot(v1, v2)

    def decide(self, question: str) -> AgentStrategy:
        """Decides strategy based on semantic intent and question length.

        Args:
            question (str): The user's question.

        Returns:
            AgentStrategy: The chosen strategy (GREETING, RAG or DIRECT).
        """
        # 1. Check for Greeting Intent
        question_vec = np.array(self.embeddings_service.get_embedding(question))
        max_sim = 0
        for g_vec in self._get_greeting_vectors():
            sim = self._cosine_similarity(question_vec, g_vec)
            max_sim = max(max_sim, sim)

        # Threshold for greeting similarity
        if max_sim > 0.75:
            return AgentStrategy.GREETING

        # 2. Fallback to length for RAG vs DIRECT
        if len(question) > self.rag_threshold:
            return AgentStrategy.RAG
        return AgentStrategy.DIRECT

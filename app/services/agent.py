from app.schemas.agent import AgentStrategy


class Agent:
    """Agent responsible for deciding the processing strategy for a user question."""

    def __init__(self, rag_threshold: int = 50):
        """Initializes the Agent with a threshold for RAG usage.

        Args:
            rag_threshold (int): The character length threshold. Questions longer
                than this will trigger the RAG strategy. Defaults to 50.
        """
        self.rag_threshold = rag_threshold

    def decide(self, question: str) -> AgentStrategy:
        """Decides whether to use RAG or DIRECT answering based on question length.

        Args:
            question (str): The user's question.

        Returns:
            AgentStrategy: The chosen strategy (RAG or DIRECT).
        """
        if len(question) > self.rag_threshold:
            return AgentStrategy.RAG
        return AgentStrategy.DIRECT

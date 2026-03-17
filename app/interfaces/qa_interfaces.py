from typing import Protocol


class LLMProtocol(Protocol):
    """Protocol defining the interface for a Large Language Model generator."""

    def generate(self, prompt: str) -> str:
        """Generates a text response based on the provided prompt.

        Args:
            prompt (str): The input text prompt for the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        ...


class RAGProtocol(Protocol):
    """Protocol defining the interface for a Retrieval-Augmented Generation retriever."""

    def retrieve(self, question: str) -> list[str]:
        """Retrieves relevant document chunks based on the question.

        Args:
            question (str): The user's query or question.

        Returns:
            list[str]: A list of relevant text chunks retrieved from the knowledge base.
        """
        ...

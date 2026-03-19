from sentence_transformers import SentenceTransformer


class EmbeddingsService:
    """Service responsible for generating vector embeddings using local models."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """Initializes the service and loads the embedding model.

        Args:
            model_name (str): The name of the sentence-transformers model to use.
                Defaults to a multilingual model optimized for Portuguese.
        """
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text: str) -> list[float]:
        """Generates a high-dimensional vector embedding for the given text.

        Args:
            text (str): The input text to be vectorized.

        Returns:
            list[float]: A 384-dimensional list of floats representing the text.
        """
        # encode returns a numpy array, we convert to list for database compatibility
        embedding = self.model.encode(text)
        return embedding.tolist()

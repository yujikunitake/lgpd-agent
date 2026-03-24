import httpx

from app.interfaces.qa_interfaces import LLMProtocol


class LLMService(LLMProtocol):
    """Service to interact with LLMs via Local Ollama API."""

    def __init__(
        self,
        model: str = "phi3:mini",
        api_key: str | None = None,
        base_url: str = "http://localhost:11434/v1/chat/completions",
    ):
        """Initializes the LLMService.

        Args:
            model (str): The model identifier to use (e.g., phi3, llama3).
            api_key (str | None): Optional API key (if using a proxy).
            base_url (str): The local or remote base URL.
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
        """Generates a response from the LLM.

        Args:
            prompt (str): The user prompt.

        Returns:
            str: The LLM's response content.

        Raises:
            Exception: If the API call fails or returns an error.
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}

        try:
            with httpx.Client() as client:
                response = client.post(self.base_url, headers=headers, json=data, timeout=60.0)

            if response.status_code != 200:
                raise Exception(f"LLM generation failed: {response.status_code} - {response.text}")

            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            if "LLM generation failed" in str(e):
                raise
            raise Exception(f"LLM generation failed: {e}") from e

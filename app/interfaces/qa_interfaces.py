from typing import Protocol


class LLMProtocol(Protocol):
    def generate(self, prompt: str) -> str: ...


class RAGProtocol(Protocol):
    def retrieve(self, question: str) -> list[str]: ...

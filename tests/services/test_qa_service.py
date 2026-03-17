from app.services.agent import Agent
from app.services.qa_service import QAService


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "Resposta mockada"


class FakeRag:
    def retrieve(self, question: str):
        return ["Trecho da LGPD"]


def test_qa_service_uses_rag_for_long_questions():
    # threshold 50, string has > 50 chars -> will use RAG
    long_question = "Esta é uma pergunta super longa que propositalmente passa de 50 caracteres."

    service = QAService(llm=FakeLLM(), rag=FakeRag(), agent=Agent(rag_threshold=50))

    response = service.ask(long_question)

    assert response.answer == "Resposta mockada"
    assert response.sources == ["Trecho da LGPD"]


def test_qa_service_bypasses_rag_for_short_questions():
    # threshold 50, string < 50 chars -> will skip RAG
    short_question = "O que é isso?"

    service = QAService(llm=FakeLLM(), rag=FakeRag(), agent=Agent(rag_threshold=50))

    response = service.ask(short_question)

    assert response.answer == "Resposta mockada"
    assert response.sources == []  # Expected empty per Agent rules

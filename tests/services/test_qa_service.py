from app.services.qa_service import QAService


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "Resposta mockada"


class FakeRag:
    def retrieve(self, question: str):
        return ["Trecho da LGPD"]


def test_qa_service_returns_answer_and_sources():
    service = QAService(
        llm=FakeLLM(),
        rag=FakeRag(),
    )

    response = service.ask("O que é LGPD?")

    assert hasattr(response, "answer")
    assert hasattr(response, "sources")

    assert response.answer == "Resposta mockada"
    assert response.sources == ["Trecho da LGPD"]

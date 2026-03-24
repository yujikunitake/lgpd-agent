from unittest.mock import MagicMock

import pytest

from app.services.qa_service import QAService


@pytest.fixture
def mock_rag():
    rag = MagicMock()
    rag.retrieve.return_value = ["Art. 1º Esta Lei dispõe sobre o tratamento de dados pessoais..."]
    return rag


@pytest.fixture
def mock_agent():
    from app.services.agent import Agent

    agent = MagicMock(spec=Agent)
    from app.schemas.agent import AgentStrategy

    agent.decide.return_value = AgentStrategy.RAG
    return agent


@pytest.fixture
def qa_service(mock_llm, mock_rag, mock_agent):
    return QAService(mock_llm, mock_rag, mock_agent)


def test_qa_service_answers_from_context(qa_service, mock_llm, mock_rag, mock_agent):
    from app.schemas.qa import QAResponse

    response = qa_service.ask("O que é a LGPD?")

    assert isinstance(response, QAResponse)
    assert response.answer == "De acordo com a LGPD, o tratamento deve ser ético."

    args, _ = mock_llm.generate.call_args
    prompt = args[0]
    assert "Art. 1º" in prompt
    assert "O que é a LGPD?" in prompt
    assert "Contexto" in prompt

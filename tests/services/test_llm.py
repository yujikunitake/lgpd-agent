import pytest
import respx
from httpx import Response

from app.services.llm import LLMService


@pytest.fixture
def llm_service():
    return LLMService(model="phi3:mini")


@respx.mock
def test_llm_generate_returns_content(llm_service):
    # Mock Ollama local API response
    mock_response = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "A LGPD é a Lei Geral de Proteção de Dados.",
                }
            }
        ]
    }

    route = respx.post("http://localhost:11434/v1/chat/completions").mock(
        return_value=Response(200, json=mock_response)
    )

    response = llm_service.generate("O que é LGPD?")

    assert response == "A LGPD é a Lei Geral de Proteção de Dados."
    assert route.called

    # Check if body was correct
    last_request = route.calls.last.request
    import json

    body = json.loads(last_request.content)
    assert body["model"] == "phi3:mini"
    assert body["messages"][0]["content"] == "O que é LGPD?"


@respx.mock
def test_llm_generate_handles_error(llm_service):
    respx.post("http://localhost:11434/v1/chat/completions").mock(return_value=Response(500))

    with pytest.raises(Exception, match="LLM generation failed"):
        llm_service.generate("Prompt")

import pytest
import respx
from app.services.llm import LLMService
from httpx import Response


@pytest.fixture
def llm_service():
    return LLMService(api_key="sk-test-key", model="google/gemini-flash-1.5")


@respx.mock
def test_llm_generate_returns_content(llm_service):
    # Mock OpenRouter API response
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

    route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(200, json=mock_response)
    )

    response = llm_service.generate("O que é LGPD?")

    assert response == "A LGPD é a Lei Geral de Proteção de Dados."
    assert route.called

    # Check if headers and body were correct
    last_request = route.calls.last.request
    assert last_request.headers["Authorization"] == "Bearer sk-test-key"
    import json

    body = json.loads(last_request.content)
    assert body["model"] == "google/gemini-flash-1.5"
    assert body["messages"][0]["content"] == "O que é LGPD?"


@respx.mock
def test_llm_generate_handles_error(llm_service):
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(return_value=Response(500))

    with pytest.raises(Exception, match="LLM generation failed"):
        llm_service.generate("Prompt")

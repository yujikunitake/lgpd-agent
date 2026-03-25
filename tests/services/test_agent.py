from unittest.mock import MagicMock

import numpy as np
import pytest

from app.schemas.agent import AgentStrategy
from app.services.agent import Agent


@pytest.fixture
def mock_embeddings():
    service = MagicMock()
    # Default return a random vector
    service.get_embeddings.return_value = np.array([0.1] * 384)
    return service


def test_should_detect_greeting_semantically(mock_embeddings):
    agent = Agent(mock_embeddings)

    # Mock greeting vectors: [1, 0, 0]
    agent._get_greeting_vectors = MagicMock(return_value=[np.array([1, 0, 0, 0])])

    # Input vector: [0.9, 0, 0, 0] -> Sim = 0.9 (> 0.75)
    mock_embeddings.get_embedding.return_value = np.array([0.9, 0, 0, 0])

    assert agent.decide("Opa!") == AgentStrategy.GREETING


def test_should_not_detect_greeting_for_long_text(mock_embeddings):
    agent = Agent(mock_embeddings)

    # Mock greeting vectors: [1, 0, 0]
    agent._get_greeting_vectors = MagicMock(return_value=[np.array([1, 0, 0, 0])])

    # Input vector: [0.1, 0.1, 0.1, 0.1] -> Low similarity
    mock_embeddings.get_embedding.return_value = np.array([0.1, 0.1, 0.1, 0.1])

    long_question = "Explique detalhadamente como funciona a LGPD no Brasil hoje em dia"
    assert agent.decide(long_question) == AgentStrategy.RAG


def test_should_use_direct_for_short_question(mock_embeddings):
    agent = Agent(mock_embeddings)

    # Low similarity to greetings
    agent._get_greeting_vectors = MagicMock(return_value=[np.array([1, 0, 0, 0])])
    mock_embeddings.get_embedding.return_value = np.array([0, 1, 0, 0])

    assert agent.decide("Artigo 1?") == AgentStrategy.DIRECT


def test_rag_threshold_logic(mock_embeddings):
    agent = Agent(mock_embeddings, rag_threshold=10)

    # Low similarity to greetings
    agent._get_greeting_vectors = MagicMock(return_value=[np.array([1, 0, 0, 0])])
    mock_embeddings.get_embedding.return_value = np.array([0, 1, 0, 0])

    assert agent.decide("1234567890") == AgentStrategy.DIRECT
    assert agent.decide("12345678901") == AgentStrategy.RAG

from app.schemas.agent import AgentStrategy
from app.services.agent import Agent


def test_should_use_rag_for_long_question():
    agent = Agent()
    decision = agent.decide("Explique detalhadamente o que são dados sensíveis na LGPD")
    assert decision == AgentStrategy.RAG


def test_should_not_use_rag_for_short_question():
    agent = Agent()
    decision = agent.decide("O que é LGPD?")
    assert decision == AgentStrategy.DIRECT


def test_should_use_direct_for_boundary_question():
    agent = Agent(rag_threshold=50)
    decision = agent.decide("a" * 50)
    assert decision == AgentStrategy.DIRECT


def test_boundary_question():
    agent = Agent(rag_threshold=50)
    assert agent.decide("x" * 50) == AgentStrategy.DIRECT
    assert agent.decide("x" * 51) == AgentStrategy.RAG

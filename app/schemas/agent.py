from enum import StrEnum


class AgentStrategy(StrEnum):
    """Strategy chosen by the agent to determine the processing flow."""

    RAG = "use_rag"
    DIRECT = "direct"
    GREETING = "greeting"

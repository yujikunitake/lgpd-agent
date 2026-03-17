from enum import StrEnum


class AgentStrategy(StrEnum):
    RAG = "use_rag"
    DIRECT = "direct"

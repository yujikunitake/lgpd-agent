from app.schemas.agent import AgentStrategy


class Agent:
    def __init__(self, rag_threshold: int = 50):
        self.rag_threshold = rag_threshold

    def decide(self, question: str) -> AgentStrategy:
        if len(question) > self.rag_threshold:
            return AgentStrategy.RAG
        return AgentStrategy.DIRECT

from app.interfaces.qa_interfaces import LLMProtocol, RAGProtocol
from app.schemas.qa import QAResponse, Source
from app.services.agent import Agent


class QAService:
    """Service to orchestrate the QA process using Agent decision and RAG."""

    def __init__(
        self,
        llm_service: LLMProtocol,
        rag_service: RAGProtocol,
        agent: Agent,
    ):
        """Initializes the QAService.

        Args:
            llm_service (LLMProtocol): Service to generate answers.
            rag_service (RAGProtocol): Service to retrieve context.
            agent (Agent): Service to decide strategy.
        """
        self.llm_service = llm_service
        self.rag_service = rag_service
        self.agent = agent

    def ask(self, question: str) -> QAResponse:
        """Processes a question and returns a structured response.

        Args:
            question (str): The user's question.

        Returns:
            QAResponse: The generated answer and metadata.
        """
        # 1. Decide strategy (covers GREETING, RAG, DIRECT)
        strategy = self.agent.decide(question)

        # 2. Handle GREETING strategy
        from app.schemas.agent import AgentStrategy

        if strategy == AgentStrategy.GREETING:
            return QAResponse(
                answer="Olá! Eu sou o assistente LGPD. Posso te ajudar com dúvidas sobre a\
                    Lei Geral de Proteção de Dados. O que você gostaria de saber?",
                strategy=strategy,
                sources=[],
            )

        # 3. Handle DIRECT strategy
        if strategy == AgentStrategy.DIRECT:
            prompt = f"Pergunta: {question}\nResposta breve em Português:"
            answer = self.llm_service.generate(prompt)
            return QAResponse(answer=answer, strategy=strategy, sources=[])

        # 3. Handle RAG strategy
        # Retrieve context
        context_chunks = self.rag_service.retrieve(question)

        if not context_chunks:
            return QAResponse(
                answer="Desculpe, não encontrei informações sobre isso na LGPD.",
                strategy=strategy,
                sources=[],
            )

        # Format context for prompt
        context_str = "\n".join([f"- {c}" for c in context_chunks])

        # Build Prompt (Simplified for 1B model)
        prompt = f"""Use o contexto da LGPD para responder em Português. Seja breve.

        Contexto:
        {context_str}

        Pergunta: {question}
        Resposta:"""

        # Generate answer
        answer = self.llm_service.generate(prompt)

        # For now, sources are just the strings retrieved.
        # In the future we can extract more metadata.
        sources = [Source(content=c[:100] + "...", location="LGPD") for c in context_chunks]

        return QAResponse(answer=answer, strategy=strategy, sources=sources)

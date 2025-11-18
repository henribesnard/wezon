"""Chat orchestration service placeholder.

The actual implementation will:
* Build a semantic search query against the vector store (pgvector/Qdrant)
* Optionally call web search agents when freshness is low
* Construct a prompt with article excerpts and metadata
* Delegate generation to an LLM provider
"""
from __future__ import annotations

from typing import List

from app.schemas import ChatRequest, ChatResponse, ChatAnswerSource


async def answer_question(payload: ChatRequest) -> ChatResponse:
    """Return a deterministic placeholder response.

    Keeping the interface async allows wiring to real AI components later
    without changing router signatures.
    """

    sources: List[ChatAnswerSource] = [
        ChatAnswerSource(
            title="Placeholder article",
            url="https://example.com/article",
            trust_score=0.7,
        )
    ]
    answer = (
        "This is a stubbed answer. The production pipeline will combine RAG, "
        "language selection, and web retrieval as described in the specification."
    )
    return ChatResponse(answer=answer, sources=sources)

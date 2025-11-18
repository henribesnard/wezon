"""Chat endpoint wiring to the orchestration placeholder."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas import ChatRequest, ChatResponse
from app.services.chat import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return await answer_question(request)

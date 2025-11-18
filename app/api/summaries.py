"""Daily summary endpoints."""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import ScopeType
from app.schemas import DailySummaryRead
from app.services.summaries import list_daily_summaries

router = APIRouter(prefix="/daily-summaries", tags=["summaries"])


@router.get("/", response_model=List[DailySummaryRead])
async def get_daily_summaries(
    summary_date: Optional[date] = Query(None, alias="date"),
    scope_type: Optional[ScopeType] = Query(None),
    scope_id: Optional[int] = Query(None),
    language: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[DailySummaryRead]:
    summaries = await list_daily_summaries(
        session,
        summary_date=summary_date,
        scope_type=scope_type,
        scope_id=scope_id,
        language=language,
    )
    return [DailySummaryRead.from_orm(item) for item in summaries]

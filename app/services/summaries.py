"""Summaries service for daily digest retrieval."""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DailySummary, ScopeType


async def list_daily_summaries(
    session: AsyncSession,
    *,
    summary_date: Optional[date] = None,
    scope_type: Optional[ScopeType] = None,
    scope_id: Optional[int] = None,
    language: Optional[str] = None,
) -> List[DailySummary]:
    query = select(DailySummary)
    if summary_date:
        query = query.where(DailySummary.date == summary_date)
    if scope_type:
        query = query.where(DailySummary.scope_type == scope_type)
    if scope_id:
        query = query.where(DailySummary.scope_id == scope_id)
    result = await session.scalars(query)
    return list(result)

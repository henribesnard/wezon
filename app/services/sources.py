"""Source service encapsulating CRUD operations for news feeds."""
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Source


async def list_sources(session: AsyncSession) -> List[Source]:
    result = await session.scalars(select(Source))
    return list(result)


async def create_source(session: AsyncSession, source: Source) -> Source:
    session.add(source)
    await session.flush()
    return source


async def update_source(session: AsyncSession, db_source: Source, data: dict) -> Source:
    for key, value in data.items():
        setattr(db_source, key, value)
    await session.flush()
    return db_source

"""Source service encapsulating CRUD operations for news feeds."""
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Source


async def list_sources(session: AsyncSession) -> List[Source]:
    result = await session.scalars(select(Source).order_by(Source.id))
    return list(result)


async def create_source(session: AsyncSession, source: Source) -> Source:
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source


async def update_source(session: AsyncSession, db_source: Source, data: dict) -> Source:
    for key, value in data.items():
        setattr(db_source, key, value)
    await session.commit()
    await session.refresh(db_source)
    return db_source

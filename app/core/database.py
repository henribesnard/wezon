"""Database engine and session management utilities.

The database schema mirrors the specification: countries, sources, articles,
translations, categories, entities, and daily summaries. Async SQLAlchemy is
used so that API endpoints can coexist with future background agents.
"""
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base declarative class used by all ORM models."""


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False, future=True)
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield a scoped SQLAlchemy async session.

    This dependency is injected in routers to illustrate how queries will be
    executed once real data pipelines are connected.
    """

    async with AsyncSessionMaker() as session:
        yield session

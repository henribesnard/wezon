"""Article service with stubbed data access.

Real ingestion agents will populate the relational database. For now, the
service returns structured placeholders that respect the API contract so that
front-end or orchestration teams can integrate incrementally.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article, ArticleCategory, ArticleEntity


async def list_articles(
    session: AsyncSession,
    *,
    country: Optional[str] = None,
    category: Optional[str] = None,
    language: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[Article]:
    """Return a filtered list of articles.

    Filters are applied progressively to mirror the /articles endpoint.
    """

    query = select(Article).limit(limit).offset(offset)
    # Filters would be added here when the related tables are populated.
    result = await session.scalars(query)
    return list(result)


async def get_article(session: AsyncSession, article_id: int) -> Article | None:
    """Return a single article with its relations if available."""

    query = select(Article).where(Article.id == article_id)
    result = await session.scalars(query)
    return result.first()


def categories_to_list(categories: Iterable[ArticleCategory]) -> list[str]:
    return [c.category for c in categories]


def entities_to_list(entities: Iterable[ArticleEntity]) -> list[str]:
    return [e.value for e in entities]

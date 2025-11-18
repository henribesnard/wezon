"""Article service with stubbed data access.

Real ingestion agents will populate the relational database. For now, the
service returns structured placeholders that respect the API contract so that
front-end or orchestration teams can integrate incrementally.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article, ArticleCategory, ArticleEntity, Country, Language


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

    query = (
        select(Article)
        .options(
            selectinload(Article.categories),
            selectinload(Article.entities),
            selectinload(Article.source),
        )
        .limit(limit)
        .offset(offset)
        .order_by(Article.published_at.desc().nullslast())
    )
    if country:
        query = query.join(Country).where(Country.iso == country.upper())
    if category:
        query = query.join(ArticleCategory).where(ArticleCategory.category == category)
    if language:
        query = query.join(Language).where(Language.code == language)
    if date_from:
        query = query.where(Article.published_at >= date_from)
    if date_to:
        query = query.where(Article.published_at <= date_to)

    query = query.distinct()
    result = await session.scalars(query)
    return list(result)


async def get_article(session: AsyncSession, article_id: int) -> Article | None:
    """Return a single article with its relations if available."""

    query = (
        select(Article)
        .options(
            selectinload(Article.categories),
            selectinload(Article.entities),
            selectinload(Article.source),
        )
        .where(Article.id == article_id)
    )
    result = await session.scalars(query)
    return result.first()


def categories_to_list(categories: Iterable[ArticleCategory]) -> list[str]:
    return [c.category for c in categories]


def entities_to_list(entities: Iterable[ArticleEntity]) -> list[str]:
    return [e.value for e in entities]

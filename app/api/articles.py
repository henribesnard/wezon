"""Articles endpoints as described in the specification."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas import ArticleRead
from app.services.articles import (
    categories_to_list,
    entities_to_list,
    get_article,
    list_articles,
)

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=List[ArticleRead])
async def get_articles(
    country: Optional[str] = Query(None, description="Country ISO code"),
    category: Optional[str] = Query(None, description="Category name"),
    language: Optional[str] = Query(None, description="Language code"),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> List[ArticleRead]:
    offset = (page - 1) * page_size
    articles = await list_articles(
        session,
        country=country,
        category=category,
        language=language,
        date_from=date_from,
        date_to=date_to,
        limit=page_size,
        offset=offset,
    )
    return [
        ArticleRead(
            id=article.id,
            source_id=article.source_id,
            country_id=article.country_id,
            language_id=article.language_id,
            title=article.title,
            summary=article.summary,
            url=article.url,
            published_at=article.published_at,
            trust_score=article.trust_score,
            processing_status=article.processing_status,
            categories=categories_to_list(article.categories or []),
            entities=entities_to_list(article.entities or []),
        )
        for article in articles
    ]


@router.get("/{article_id}", response_model=ArticleRead)
async def get_article_detail(
    article_id: int, session: AsyncSession = Depends(get_session)
) -> ArticleRead:
    article = await get_article(session, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleRead(
        id=article.id,
        source_id=article.source_id,
        country_id=article.country_id,
        language_id=article.language_id,
        title=article.title,
        summary=article.summary,
        url=article.url,
        published_at=article.published_at,
        trust_score=article.trust_score,
        processing_status=article.processing_status,
        categories=categories_to_list(article.categories or []),
        entities=entities_to_list(article.entities or []),
    )

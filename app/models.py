"""SQLAlchemy ORM models reflecting the technical specification.

Only the essential fields are included to provide a coherent schema for the
FastAPI skeleton. The models intentionally avoid advanced constraints so they
can be extended once the ingestion and AI agents are connected.
"""
from __future__ import annotations

import enum
from datetime import datetime, date

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SourceType(str, enum.Enum):
    """Types of sources supported by the ingestion agents."""

    RSS = "rss"
    WEB = "web"
    API = "api"


class ProcessingStatus(str, enum.Enum):
    """Lifecycle of an article inside the pipeline."""

    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


class EntityType(str, enum.Enum):
    """Named entity categories used for tagging."""

    PERSON = "person"
    ORGANIZATION = "org"
    LOCATION = "location"
    KEYWORD = "keyword"


class ScopeType(str, enum.Enum):
    """Scope for daily summaries."""

    CONTINENT = "continent"
    REGION = "region"
    COUNTRY = "country"


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    iso: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)

    sources: Mapped[list[Source]] = relationship("Source", back_populates="country")
    articles: Mapped[list[Article]] = relationship("Article", back_populates="country")


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    sources: Mapped[list[Source]] = relationship("Source", back_populates="language")
    articles: Mapped[list[Article]] = relationship("Article", back_populates="language")
    daily_summaries: Mapped[list[DailySummary]] = relationship(
        "DailySummary", back_populates="language"
    )


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    language_id: Mapped[int | None] = mapped_column(ForeignKey("languages.id"))
    trust_score: Mapped[float | None] = mapped_column(Float)
    fetch_frequency: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    country: Mapped[Country | None] = relationship("Country", back_populates="sources")
    language: Mapped[Language | None] = relationship("Language", back_populates="sources")
    articles: Mapped[list[Article]] = relationship("Article", back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    language_id: Mapped[int | None] = mapped_column(ForeignKey("languages.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String(500))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    trust_score: Mapped[float | None] = mapped_column(Float)
    raw_html: Mapped[str | None] = mapped_column(Text)
    processing_status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False
    )

    categories: Mapped[list[ArticleCategory]] = relationship("ArticleCategory", back_populates="article")
    entities: Mapped[list[ArticleEntity]] = relationship("ArticleEntity", back_populates="article")
    translations: Mapped[list[ArticleTranslation]] = relationship("ArticleTranslation", back_populates="article")
    source: Mapped[Source | None] = relationship("Source", back_populates="articles")
    country: Mapped[Country | None] = relationship("Country", back_populates="articles")
    language: Mapped[Language | None] = relationship("Language", back_populates="articles")


class ArticleCategory(Base):
    __tablename__ = "article_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)

    article: Mapped[Article] = relationship("Article", back_populates="categories")


class ArticleEntity(Base):
    __tablename__ = "article_entities"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False)
    type: Mapped[EntityType] = mapped_column(Enum(EntityType), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    article: Mapped[Article] = relationship("Article", back_populates="entities")


class ArticleTranslation(Base):
    __tablename__ = "article_translations"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    translated_title: Mapped[str | None] = mapped_column(String(500))
    translated_content: Mapped[str | None] = mapped_column(Text)
    translated_summary: Mapped[str | None] = mapped_column(Text)

    article: Mapped[Article] = relationship("Article", back_populates="translations")


class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    scope_type: Mapped[ScopeType] = mapped_column(Enum(ScopeType), nullable=False)
    scope_id: Mapped[int | None] = mapped_column(Integer)
    language_id: Mapped[int | None] = mapped_column(ForeignKey("languages.id"))
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)

    language: Mapped[Language | None] = relationship("Language", back_populates="daily_summaries")

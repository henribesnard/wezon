"""Pydantic schemas used by the FastAPI routers.

The schemas are intentionally small and read-only, but they document the
expected shape of the API responses and requests listed in the technical
specification.
"""
from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from app.models import EntityType, ProcessingStatus, ScopeType, SourceType


class CountryRead(BaseModel):
    id: int
    name: str
    iso: str
    region: str

    class Config:
        orm_mode = True


class SourceRead(BaseModel):
    id: int
    name: str
    url: str
    type: SourceType
    country_id: Optional[int]
    language_id: Optional[int]
    trust_score: Optional[float]
    fetch_frequency: Optional[int]
    is_active: bool

    class Config:
        orm_mode = True


class SourceCreate(BaseModel):
    name: str
    url: str
    type: SourceType
    country_id: Optional[int] = None
    language_id: Optional[int] = None
    fetch_frequency: Optional[int] = Field(
        None, description="Frequency in seconds for ingestion tasks"
    )


class ArticleRead(BaseModel):
    id: int
    source_id: Optional[int]
    country_id: Optional[int]
    language_id: Optional[int]
    title: str
    summary: Optional[str]
    url: Optional[str]
    published_at: Optional[datetime]
    trust_score: Optional[float]
    processing_status: ProcessingStatus
    categories: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)

    class Config:
        orm_mode = True


class DailySummaryRead(BaseModel):
    id: int
    date: date
    scope_type: ScopeType
    scope_id: Optional[int]
    language_id: Optional[int]
    summary_text: str

    class Config:
        orm_mode = True


class ChatRequest(BaseModel):
    question: str
    language: str
    country: Optional[str] = None
    region: Optional[str] = None
    time_range: Optional[str] = Field(None, description="Ex: 24h, 7d, 1m")


class ChatAnswerSource(BaseModel):
    title: str
    url: str
    trust_score: Optional[float]


class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatAnswerSource]


class HealthResponse(BaseModel):
    status: str
    checks: dict[str, Any]

"""Endpoints for managing ingestion sources."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_session
from app.models import Source
from app.schemas import SourceCreate, SourceRead
from app.services.sources import create_source, list_sources, update_source

router = APIRouter(prefix="/sources", tags=["sources"])
admin_router = APIRouter(prefix="/admin/sources", tags=["admin:sources"])


async def _require_admin_token(
    x_admin_token: str | None = Header(None, description="Temporary admin token"),
):
    settings = get_settings()
    if x_admin_token != settings.admin_jwt_secret:
        raise HTTPException(status_code=401, detail="Admin token invalid")


@router.get("/", response_model=list[SourceRead])
async def list_source_endpoint(session: AsyncSession = Depends(get_session)) -> list[SourceRead]:
    sources = await list_sources(session)
    return [SourceRead.from_orm(source) for source in sources]


@admin_router.post("/", response_model=SourceRead, dependencies=[Depends(_require_admin_token)])
async def create_source_endpoint(
    payload: SourceCreate, session: AsyncSession = Depends(get_session)
) -> SourceRead:
    db_source = Source(**payload.dict())
    await create_source(session, db_source)
    return SourceRead.from_orm(db_source)


@admin_router.put("/{source_id}", response_model=SourceRead, dependencies=[Depends(_require_admin_token)])
async def update_source_endpoint(
    source_id: int,
    payload: SourceCreate,
    session: AsyncSession = Depends(get_session),
) -> SourceRead:
    sources = await list_sources(session)
    db_source = next((s for s in sources if s.id == source_id), None)
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    updated = await update_source(session, db_source, payload.dict())
    return SourceRead.from_orm(updated)

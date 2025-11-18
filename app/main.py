"""FastAPI application entrypoint.

Routers mirror the endpoints proposed in the specification:
* /articles and /articles/{id}
* /daily-summaries
* /chat
* /sources (public list) and /admin/sources (protected)
"""
from __future__ import annotations

from fastapi import Depends, FastAPI

from app.api import articles, chat, health, sources, summaries
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.include_router(health.router)
app.include_router(articles.router)
app.include_router(summaries.router)
app.include_router(chat.router)
app.include_router(sources.router)
app.include_router(sources.admin_router)


@app.get("/", tags=["meta"])
async def root():
    return {"message": "Wezon backend skeleton is running", "docs": "/docs"}

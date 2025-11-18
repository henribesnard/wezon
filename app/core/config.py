"""Application configuration settings.

These settings centralize the environment variables that are required by the
FastAPI backend skeleton. They are intentionally minimal but highlight the
main integration points described in the functional and technical
specifications (PostgreSQL, Redis for task orchestration, vector store for
RAG, and credentials for admin access).
"""
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables.

    Attributes:
        app_name: Human friendly application name used in the OpenAPI docs.
        database_url: Connection string for the PostgreSQL instance that hosts
            the relational schema (countries, sources, articles, etc.).
        redis_url: Redis URL for background queues and orchestration (Celery /
            RQ). This is a placeholder to align with the scheduling and
            monitoring requirements.
        vector_store_url: Endpoint for the vector database (pgvector, Qdrant,
            Milvus, etc.) used by the RAG subsystem.
        admin_jwt_secret: Secret used to sign JWT tokens for the admin routes.
    """

    app_name: str = Field("Wezon Backend API", env="APP_NAME")
    database_url: str = Field(
        "postgresql+asyncpg://user:password@localhost:5432/wezon", env="DATABASE_URL"
    )
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    vector_store_url: str = Field(
        "http://localhost:6333", env="VECTOR_STORE_URL"
    )
    admin_jwt_secret: str = Field("CHANGE_ME", env="ADMIN_JWT_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Return a singleton settings instance for dependency injection."""

    return Settings()

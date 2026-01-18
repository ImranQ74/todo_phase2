"""Database connection and session management for Neon PostgreSQL."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config import get_settings

# Global engine instance
engine = None


def get_engine():
    """Get or create the async database engine.

    Returns:
        AsyncEngine: SQLAlchemy async engine for PostgreSQL connection
    """
    global engine
    if engine is None:
        settings = get_settings()
        engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            connect_args={"ssl": "require"},
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return engine


# Session factory for creating async database sessions
AsyncSessionLocal = sessionmaker(
    bind=get_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """Dependency for FastAPI to get a database session.

    Yields:
        AsyncSession: Database session for the request

    Usage:
        Add as dependency to route handlers:
        async def my_endpoint(db: AsyncSession = Depends(get_db))
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables.

    Creates all tables defined in SQLModel metadata.
    Should be called during application startup.
    """
    from src.models.task import Task

    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """Close database connections.

    Should be called during application shutdown.
    """
    if engine:
        await engine.dispose()

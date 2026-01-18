"""FastAPI application entry point for the Todo backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import close_db, init_db
from src.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events.

    This function handles:
    - Startup: Initialize database tables
    - Shutdown: Close database connections
    """
    # Startup
    settings = get_settings()
    if settings.debug:
        print("Starting up...")
    await init_db()

    yield

    # Shutdown
    if settings.debug:
        print("Shutting down...")
    await close_db()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()

    app = FastAPI(
        title="Todo API",
        description="Multi-user Todo API with JWT authentication",
        version="2.0.0",
        lifespan=lifespan,
    )

    # Configure CORS
    # In production, replace origins with actual frontend domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(tasks.router)

    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint for load balancers."""
        return {"status": "healthy"}

    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint with API information."""
        return {"message": "Todo API", "version": "2.0.0"}

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )

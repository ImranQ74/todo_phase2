# Backend Specification: FastAPI with SQLModel, Neon DB, JWT Verification
## Phase 2 Section 1: Todo Full-Stack Web Application

## 1. Overview

This specification defines the complete backend implementation for Phase 2 of the "Evolution of Todo" project. The backend is a secure, multi-user Todo API built with FastAPI, SQLModel for ORM, and Neon Serverless PostgreSQL for persistent storage. All operations are authenticated via JWT and filtered by `user_id` to ensure strict user isolation.

## 2. Project Structure

```
backend/
├── .env.example              # Environment variable template
├── pyproject.toml            # UV project configuration
├── requirements.txt          # Generated dependency list
├── README.md                 # Backend documentation
├── migrations/               # Database migrations (future use)
├── src/
│   ├── __init__.py
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Environment configuration
│   ├── database.py           # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py           # SQLModel Task entity
│   │   └── user.py           # SQLModel User entity (minimal)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py           # Pydantic schemas for task input/output
│   │   └── auth.py           # Pydantic schemas for auth responses
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints (if needed)
│   │   └── tasks.py          # Task CRUD endpoints
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py           # JWT verification dependency
│   │   └── database.py       # Database session dependency
│   └── utils/
│       ├── __init__.py
│       └── jwt.py            # JWT utility functions
└── tests/
    ├── __init__.py
    ├── conftest.py           # Test fixtures
    └── test_tasks.py         # Task endpoint tests
```

## 3. Dependencies

### Core Dependencies
```toml
# pyproject.toml
[project]
name = "todo-backend"
version = "0.1.0"
description = "FastAPI backend for Todo application"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlmodel>=0.0.19",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-jose[cryptography]>=3.3.0",
    "asyncpg>=0.29.0",
    "python-multipart>=0.0.6",
    "httpx>=0.26.0",
]
```

### Development Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]
```

## 4. Environment Variables

### Required Variables
```env
# .env.example
# Database
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-256-bit-secret-key-here-at-least-32-chars
BETTER_AUTH_ALGORITHM=HS256

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## 5. Database Models

### 5.1 Task Model
```python
# src/models/task.py
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from uuid import uuid4
from pydantic import ConfigDict


class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), unique=True, index=True)
    title: str = Field(max_length=255, description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    completed: bool = Field(default=False, description="Completion status")
    user_id: str = Field(index=True, description="User ID from JWT")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
```

### 5.2 User Model (Minimal)
```python
# src/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """Minimal user entity for reference (auth handled by Better Auth frontend)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default=None, unique=True, index=True)
    email: str = Field(unique=True, max_length=255)
    hashed_password: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
```

## 6. Pydantic Schemas

### 6.1 Task Schemas
```python
# src/schemas/task.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: Optional[bool] = Field(default=None)


class TaskResponse(BaseModel):
    """Schema for task responses."""
    id: int
    uuid: str
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""
    tasks: list[TaskResponse]
    total: int


class TaskCompleteResponse(BaseModel):
    """Schema for task completion toggle response."""
    id: int
    uuid: str
    completed: bool
```

### 6.2 Auth Schemas
```python
# src/schemas/auth.py
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """JWT token payload schema."""
    sub: str  # user_id
    exp: Optional[int] = None


class TokenResponse(BaseModel):
    """Schema for token validation response."""
    valid: bool
    user_id: Optional[str] = None
```

## 7. Configuration

```python
# src/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""
    database_url: str
    better_auth_secret: str
    better_auth_algorithm: str = "HS256"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    model_config = {
        "env_file": ".env",
        "env_prefix": "TODO_",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

## 8. Database Connection

```python
# src/database.py
from sqlmodel import create_engine, AsyncSession, sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import get_settings


def get_database_url() -> str:
    """Get the async database URL for SQLModel."""
    settings = get_settings()
    return settings.database_url


# Create async engine for Neon Serverless PostgreSQL
database_url = get_database_url()
async_engine = create_engine(
    database_url,
    echo=settings.debug if hasattr(settings, "debug") else False,
    connect_args={"ssl": "require"},
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    from src.models.task import Task
    from sqlmodel import text

    async with async_engine.begin() as conn:
        await conn.run_sync(Task.metadata.create_all)


async def close_db():
    """Close database connections."""
    await async_engine.dispose()
```

## 9. JWT Authentication

### 9.1 JWT Utilities
```python
# src/utils/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.config import get_settings


def decode_jwt(token: str) -> dict:
    """Decode and verify JWT token."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.better_auth_algorithm],
        )
        return payload
    except JWTError:
        return {"sub": None}


def create_jwt(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token (for testing purposes)."""
    settings = get_settings()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)

    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(
        to_encode,
        settings.better_auth_secret,
        algorithm=settings.better_auth_algorithm,
    )
```

### 9.2 Auth Dependency
```python
# src/dependencies/auth.py
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.utils.jwt import decode_jwt
from src.models.task import Task


security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Dependency to extract and verify JWT from Authorization header.
    Returns the user_id from the token payload.
    Raises HTTPException 401 if token is invalid.
    """
    token = credentials.credentials
    payload = decode_jwt(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def verify_task_ownership(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> Task:
    """
    Verify that the task belongs to the authenticated user.
    Returns the task if owned, raises 404 otherwise.
    """
    from sqlmodel import select

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task
```

## 10. API Endpoints

### 10.1 Tasks Router
```python
# src/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from src.database import get_db
from src.models.task import Task
from src.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskCompleteResponse,
)
from src.dependencies.auth import get_current_user_id


router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    List all tasks for the authenticated user.
    Returns paginated list of tasks.
    """
    # Count total tasks for user
    count_result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    total = len(count_result.all())

    # Get paginated tasks
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()

    return TaskListResponse(tasks=tasks, total=total)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new task for the authenticated user.
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific task by ID.
    Returns 404 if task doesn't exist or doesn't belong to user.
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a task's title, description, or completion status.
    Returns 404 if task doesn't exist or doesn't belong to user.
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update fields that are provided
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a task.
    Returns 204 on success, 404 if task doesn't exist or doesn't belong to user.
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await db.delete(task)
    await db.commit()


@router.patch("/{task_id}/complete", response_model=TaskCompleteResponse)
async def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Toggle the completion status of a task.
    Returns updated task with new completion status.
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TaskCompleteResponse(
        id=task.id,
        uuid=task.uuid,
        completed=task.completed,
    )
```

## 11. Main Application Entry Point

```python
# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import init_db, close_db
from src.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Todo API",
        description="Multi-user Todo API with JWT authentication",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS
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
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
```

## 12. Running the Backend

### Development Setup
```bash
# Navigate to backend directory
cd backend

# Initialize UV project (if not already done)
uv init

# Add dependencies
uv add fastapi uvicorn sqlmodel pydantic pydantic-settings python-jose asyncpg python-multipart httpx

# Add dev dependencies
uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy

# Copy environment file
cp .env.example .env

# Edit .env with your Neon database URL and JWT secret

# Run the server
uv run uvicorn src.main:app --reload
```

### Production Setup
```bash
# Install dependencies
uv sync

# Run migrations if needed
uv run alembic upgrade head

# Start server
uv run gunicorn src.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 13. Testing

### Test Fixtures
```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.database import get_db, AsyncSessionLocal
from src.utils.jwt import create_jwt


@pytest.fixture
async def test_user_id():
    """Return a test user ID."""
    return "test-user-123"


@pytest.fixture
async def auth_headers(test_user_id):
    """Return authorization headers with valid JWT."""
    token = create_jwt(test_user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def async_client():
    """Return an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
```

### Example Test
```python
# tests/test_tasks.py
import pytest
from tests.conftest import async_client, auth_headers, test_user_id


@pytest.mark.asyncio
async def test_create_task(async_client, auth_headers, test_user_id):
    """Test creating a new task."""
    response = await async_client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "Test Task", "description": "Test description"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test description"
    assert data["completed"] == False
    assert data["user_id"] == test_user_id


@pytest.mark.asyncio
async def test_list_tasks(async_client, auth_headers, test_user_id):
    """Test listing tasks for a user."""
    # First create a task
    await async_client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "List Test Task"},
        headers=auth_headers,
    )

    response = await async_client.get(
        f"/api/{test_user_id}/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test that requests without auth token are rejected."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/test-user/tasks")

    assert response.status_code == 403  # No auth header provided
```

## 14. Error Handling

### Standard Error Responses
```python
# All endpoints return appropriate HTTP status codes:
- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 404: Not Found (resource doesn't exist or not owned)
- 500: Internal Server Error
```

## 15. Specification Metadata

| Field | Value |
|-------|-------|
| Version | 2.0.0 |
| Phase | Phase 2 Section 1 |
| Author | Spec-Kit Plus / Claude Code |
| Created | 2025-01-15 |
| Last Updated | 2025-01-15 |
| Status | Draft |

## 16. Implementation Notes

1. **User Isolation**: All database queries include `user_id` filter to ensure users can only access their own tasks.

2. **JWT Verification**: The `get_current_user_id` dependency extracts the JWT from the `Authorization: Bearer <token>` header and validates it using the shared `BETTER_AUTH_SECRET`.

3. **Neon PostgreSQL**: The async engine uses `asyncpg` driver with SSL required for Neon Serverless connection.

4. **SQLModel**: Uses SQLModel for unified Pydantic models and SQLAlchemy ORM with async support.

5. **CORS**: Configured to allow all origins for development; restrict in production.

6. **Health Check**: `/health` endpoint for load balancer health checks.

## 17. Future Enhancements (Out of Scope)

- Pagination (currently basic skip/limit)
- Task categories/tags
- Due dates
- User registration endpoint (handled by Better Auth frontend)
- Rate limiting
- API versioning
- OpenAPI documentation at `/docs`

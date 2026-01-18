# Todo Backend API

FastAPI backend for the Todo application with JWT authentication, persistent PostgreSQL storage, and user isolation.

## Overview

This backend provides a secure, multi-user Todo API with the following features:

- **FastAPI** framework with async support
- **SQLModel** ORM for database operations
- **Neon Serverless PostgreSQL** for persistent storage
- **JWT Authentication** using Better Auth tokens
- **User Isolation** - users can only access their own tasks
- **RESTful API** with proper HTTP status codes
- **Comprehensive test suite** with pytest

## Technology Stack

- **Framework**: FastAPI 0.109.0+
- **Database**: Neon Serverless PostgreSQL with asyncpg
- **ORM**: SQLModel 0.0.19+
- **Authentication**: JWT (python-jose)
- **Testing**: pytest with asyncio support
- **Python**: 3.13+
- **Package Manager**: UV

## Project Structure

```
backend/
├── .env.example              # Environment variable template
├── pyproject.toml            # UV project configuration
├── README.md                 # This file
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task SQLModel entity
│   │   └── user.py          # User SQLModel entity
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Task Pydantic schemas
│   │   └── auth.py          # Auth Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py         # Task API endpoints
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py          # JWT verification dependency
│   │   └── database.py      # Database session dependency
│   └── utils/
│       ├── __init__.py
│       └── jwt.py           # JWT utility functions
└── tests/
    ├── __init__.py
    ├── conftest.py          # Pytest fixtures
    └── test_tasks.py        # Task endpoint tests
```

## API Endpoints

### Base URL

All endpoints are prefixed with: `/api/{user_id}/`

Replace `{user_id}` with the authenticated user's ID from the JWT token.

### Authentication

All endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/{user_id}/tasks` | List all tasks | ✅ Yes |
| `POST` | `/api/{user_id}/tasks` | Create a new task | ✅ Yes |
| `GET` | `/api/{user_id}/tasks/{task_id}` | Get task details | ✅ Yes |
| `PUT` | `/api/{user_id}/tasks/{task_id}` | Update a task | ✅ Yes |
| `DELETE` | `/api/{user_id}/tasks/{task_id}` | Delete a task | ✅ Yes |
| `PATCH` | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion | ✅ Yes |

### Task Schema

```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": "user-123",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

## Installation

### Prerequisites

- Python 3.13 or higher
- UV package manager
- Neon Serverless PostgreSQL account
- BETTER_AUTH_SECRET (shared secret for JWT)

### Setup Steps

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Initialize UV project** (if not already done):
   ```bash
   uv init
   ```

3. **Install dependencies**:
   ```bash
   uv add fastapi uvicorn sqlmodel pydantic pydantic-settings python-jose asyncpg python-multipart httpx
   ```

4. **Install development dependencies**:
   ```bash
   uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy
   ```

5. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

6. **Configure environment variables** in `.env`:
   ```bash
   # Database (from Neon console)
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require

   # Authentication (generate with: openssl rand -base64 32)
   BETTER_AUTH_SECRET=your-256-bit-secret-here

   # Server
   TODO_HOST=0.0.0.0
   TODO_PORT=8000
   TODO_DEBUG=true
   ```

7. **Create database tables**:
   ```bash
   uv run python -c "from src.database import init_db; import asyncio; asyncio.run(init_db())"
   ```

## Running the Server

### Development Mode

Start the server with auto-reload:

```bash
uv run uvicorn src.main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

For production deployment:

```bash
uv run gunicorn src.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Accessing Documentation

- **OpenAPI/Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

### Run All Tests

```bash
uv run pytest tests/ -v
```

### Run Specific Test File

```bash
uv run pytest tests/test_tasks.py -v
```

### Run with Coverage

```bash
uv run pytest tests/ --cov=src --cov-report=html
```

### Test Categories

- ✅ Create tasks (with and without description)
- ✅ List tasks (empty and with data)
- ✅ Get task by ID
- ✅ Update tasks (title, description, completion)
- ✅ Delete tasks
- ✅ Toggle completion status
- ✅ User isolation (cannot access other users' tasks)
- ✅ Authentication (valid/invalid tokens)
- ✅ Pagination
- ✅ Error handling (404, 401, 403)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ Yes | - | Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | ✅ Yes | - | JWT signing secret (min 32 chars) |
| `BETTER_AUTH_ALGORITHM` | No | HS256 | JWT algorithm |
| `TODO_HOST` | No | 0.0.0.0 | Server host address |
| `TODO_PORT` | No | 8000 | Server port number |
| `TODO_DEBUG` | No | false | Debug mode flag |

### Security Notes

- Never commit `.env` file to version control
- Use strong, random secrets (at least 32 characters)
- In production, restrict CORS origins instead of using `*`
- Always use SSL (`?sslmode=require`) with Neon

## Authentication Flow

### JWT Token Verification

1. Frontend (Better Auth) generates JWT token on user login
2. Token sent in `Authorization: Bearer <token>` header
3. Backend extracts and verifies token using `BETTER_AUTH_SECRET`
4. User ID extracted from token's `sub` claim
5. All database queries filtered by this user_id

### Token Format

```json
{
  "sub": "user-123",
  "exp": 1736000000,
  "iat": 1735913600
}
```

## User Isolation

Every task operation enforces user isolation:

```python
# All queries include user_id filter
select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id  # Ensures user owns the task
)
```

This guarantees:
- Users can only see their own tasks
- Users can only modify their own tasks
- Users can only delete their own tasks
- No cross-user data leakage

## Database Schema

### Task Table

```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_uuid ON task(uuid);
```

## API Usage Examples

### Generate Test JWT Token

```python
from src.utils.jwt import create_jwt

token = create_jwt("test-user-123")
print(token)
```

### Using curl

```bash
# Create a task
curl -X POST http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'

# List tasks
curl -X GET http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Toggle completion
curl -X PATCH http://localhost:8000/api/test-user-123/tasks/1/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using Python (httpx)

```python
import httpx

headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}

# Create task
with httpx.Client() as client:
    response = client.post(
        "http://localhost:8000/api/user-123/tasks",
        json={"title": "Test Task"},
        headers=headers
    )
    print(response.json())
```

## Troubleshooting

### Database Connection Issues

**Problem**: `asyncpg.exceptions.InvalidAuthorizationSpecificationError`

**Solution**: Ensure your `DATABASE_URL` includes `?sslmode=require`:
```
postgresql+asyncpg://user:pass@host/db?sslmode=require
```

**Problem**: `sqlalchemy.exc.ProgrammingError: relation "task" does not exist`

**Solution**: Run database initialization:
```bash
uv run python -c "from src.database import init_db; import asyncio; asyncio.run(init_db())"
```

### JWT Authentication Issues

**Problem**: `JWTError: Signature verification failed`

**Solution**: Verify that `BETTER_AUTH_SECRET` matches between:
- Backend `.env` file
- Frontend Better Auth configuration

**Problem**: `401 Unauthorized: Invalid or expired token`

**Solution**:
1. Check token expiration
2. Verify token signature
3. Ensure `sub` claim exists in token payload

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from `/backend` directory, not from `/backend/src`

**Problem**: `ImportError: cannot import name 'Task' from 'src.models'`

**Solution**: Check that `__init__.py` files exist in all packages

## Code Quality

### Formatting

```bash
# Format code
uv run black src/ tests/

# Check linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
      - id: ruff-format
```

## Deployment

### Environment Preparation

1. Set `TODO_DEBUG=false` in production
2. Use production Neon database URL
3. Set strong, unique `BETTER_AUTH_SECRET`
4. Configure CORS origins (not `*`)

### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv
RUN uv pip install --system -e .

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Follow Spec-Driven Development principles
2. Update specifications before implementing features
3. Add tests for all new functionality
4. Ensure all tests pass before committing
5. Use meaningful commit messages

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check this README
2. Review API documentation at `/docs`
3. Run tests to verify setup
4. Check environment variables
5. Verify database connection

## Version History

- **2.0.0** (2025-01-15): Phase 2 - Full-stack implementation
  - FastAPI backend with persistent storage
  - JWT authentication with Better Auth
  - User isolation enforced
  - Neon PostgreSQL integration
  - Comprehensive test suite

---

**Maintained with ❤️ using Spec-Driven Development and Claude Code**

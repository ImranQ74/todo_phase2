"""Pytest fixtures for testing the Todo backend application."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.database import get_db, AsyncSessionLocal
from src.utils.jwt import create_jwt


@pytest.fixture
def test_user_id():
    """Fixture providing a test user ID.

    Returns:
        str: A test user ID for authentication
    """
    return "test-user-123"


@pytest.fixture
def another_user_id():
    """Fixture providing another test user ID for isolation testing.

    Returns:
        str: A different test user ID
    """
    return "test-user-456"


@pytest.fixture
def auth_headers(test_user_id):
    """Fixture providing authorization headers with a valid JWT token.

    Creates a JWT token for the test user and returns headers dict
    with the Authorization header set.

    Args:
        test_user_id: The test user ID fixture

    Returns:
        dict: Headers dictionary with Authorization bearer token
    """
    token = create_jwt(test_user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def another_user_headers(another_user_id):
    """Fixture providing authorization headers for a different user.

    Args:
        another_user_id: Another test user ID fixture

    Returns:
        dict: Headers dictionary with Authorization bearer token for different user
    """
    token = create_jwt(another_user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def invalid_auth_headers():
    """Fixture providing invalid authorization headers.

    Returns:
        dict: Headers dictionary with an invalid JWT token
    """
    invalid_token = "invalid.token.here"
    return {"Authorization": f"Bearer {invalid_token}"}


@pytest.fixture
async def async_client():
    """Fixture providing an async test client for the FastAPI app.

    Creates an httpx AsyncClient configured to make requests to the
    FastAPI test application.

    Yields:
        AsyncClient: Configured test client
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db():
    """Fixture providing a database session for tests.

    Creates a new database session for each test and ensures
    proper cleanup after the test completes.

    Yields:
        AsyncSession: Database session for testing
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(autouse=True)
async def setup_database():
    """Auto-use fixture to set up database tables before tests.

    This fixture runs automatically before each test to ensure
    the database schema is created.
    """
    from src.database import init_db

    await init_db()

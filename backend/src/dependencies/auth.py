"""Authentication dependencies for FastAPI endpoints."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_db
from src.models.task import Task
from src.utils.jwt import decode_jwt


security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Extract and verify JWT from Authorization header.

    This dependency extracts the JWT token from the Authorization header,
    verifies it using the shared secret, and returns the user_id from the payload.

    Args:
        credentials: HTTP Authorization credentials from the request header

    Returns:
        str: The authenticated user's ID from the JWT payload

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or expired
    """
    token = credentials.credentials

    try:
        payload = decode_jwt(token)
        user_id: Optional[str] = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_task_ownership(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> Task:
    """Verify that the task belongs to the authenticated user.

    This dependency checks that a task exists and is owned by the authenticated user
    before allowing access to it.

    Args:
        task_id: The ID of the task to verify
        user_id: User ID from JWT (injected by get_current_user_id)
        db: Database session

    Returns:
        Task: The task object if owned by the user

    Raises:
        HTTPException: 404 Not Found if task doesn't exist or doesn't belong to user
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

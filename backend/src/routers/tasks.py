"""Task API endpoints for CRUD operations."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies.auth import get_current_user_id, verify_task_ownership
from src.models.task import Task
from src.schemas.task import (
    TaskCompleteResponse,
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)

# Create router with path prefix and tags
router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all tasks for a user",
)
async def list_tasks(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: str = Depends(get_current_user_id),
):
    """Get a paginated list of all tasks for the authenticated user.

    Args:
        user_id: The user ID from the URL path (verified against JWT)
        db: Database session
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return

    Returns:
        TaskListResponse: Object containing tasks list and total count

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 403 if user_id doesn't match token
    """
    # Verify the user_id in URL matches the authenticated user
    token_user_id = Depends(get_current_user_id)
    if user_id != token_user_id.dependency:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's tasks",
        )

    # Count total tasks for the user
    count_query = select(func.count()).where(Task.user_id == user_id)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Get paginated tasks
    query = (
        select(Task)
        .where(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Task.created_at.desc())
    )
    result = await db.execute(query)
    tasks = list(result.scalars().all())

    return TaskListResponse(tasks=tasks, total=total)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """Create a new task for the authenticated user.

    Args:
        user_id: The user ID from the URL path
        task_data: Task creation data (title, description)
        db: Database session
        token_user_id: User ID from JWT token

    Returns:
        TaskResponse: The created task

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 403 if user_id doesn't match token
        HTTPException: 400 if validation fails
    """
    # Verify the user_id in URL matches the authenticated user
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create tasks for other users",
        )

    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific task",
)
async def get_task(
    task_id: int,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """Get a specific task by ID.

    Args:
        task_id: The ID of the task to retrieve
        user_id: The user ID from the URL path
        db: Database session
        token_user_id: User ID from JWT token

    Returns:
        TaskResponse: The task object

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 403 if user_id doesn't match token
        HTTPException: 404 if task not found
    """
    # Verify the user_id in URL matches the authenticated user
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's tasks",
        )

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


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
)
async def update_task(
    task_id: int,
    user_id: str,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
    task: Task = Depends(verify_task_ownership),
):
    """Update a task's title, description, or completion status.

    Args:
        task_id: The ID of the task to update
        user_id: The user ID from the URL path
        task_data: Task update data (title, description, completed)
        db: Database session
        token_user_id: User ID from JWT token
        task: Task object (verified by verify_task_ownership)

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 403 if user_id doesn't match token
        HTTPException: 404 if task not found
    """
    # Verify the user_id in URL matches the authenticated user
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other user's tasks",
        )

    # Update fields that are provided
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
async def delete_task(
    task_id: int,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
    task: Task = Depends(verify_task_ownership),
):
    """Delete a task.

    Args:
        task_id: The ID of the task to delete
        user_id: The user ID from the URL path
        db: Database session
        token_user_id: User ID from JWT token
        task: Task object (verified by verify_task_ownership)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 403 if user_id doesn't match token
        HTTPException: 404 if task not found
    """
    # Verify the user_id in URL matches the authenticated user
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other user's tasks",
        )

    await db.delete(task)
    await db.commit()


@router.patch(
    "/{task_id}/complete",
    response_model=TaskCompleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion",
)
async def toggle_task_complete(
    task_id: int,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
    task: Task = Depends(verify_task_ownership),
):
    """Toggle the completion status of a task.

    Args:
        task_id: The ID of the task to toggle
        user_id: The user ID from the URL path
        db: Database session
        token_user_id: User ID from JWT token
        task: Task object (verified by verify_task_ownership)

    Returns:
        TaskCompleteResponse: Updated task with new completion status

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 403 if user_id doesn't match token
        HTTPException: 404 if task not found
    """
    # Verify the user_id in URL matches the authenticated user
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify other user's tasks",
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

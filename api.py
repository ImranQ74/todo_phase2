"""
FastAPI wrapper for Todo application backend.

This creates a REST API wrapper around the in-memory TodoManager.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from src.todo_app.manager import TodoManager, TaskNotFoundError

app = FastAPI(
    title="Todo API",
    description="REST API for Todo application",
    version="1.0.0",
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the todo manager
manager = TodoManager()

# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

# API endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/tasks", response_model=TaskListResponse)
async def list_tasks():
    """List all tasks."""
    tasks = manager.list_tasks()
    return {
        "tasks": tasks,
        "total": len(tasks)
    }

@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new task."""
    try:
        new_task = manager.add_task(
            title=task.title,
            description=task.description or ""
        )
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Get a specific task by ID."""
    try:
        task = manager._find_task_by_id(task_id)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task."""
    try:
        updated_task = manager.update_task(
            task_id=task_id,
            new_title=task_update.title,
            new_description=task_update.description
        )

        # Handle completion status separately if provided
        if task_update.completed is not None:
            if task_update.completed != updated_task.completed:
                # Only toggle if needed
                updated_task = manager.toggle_complete(task_id)

        return updated_task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task."""
    try:
        manager.delete_task(task_id)
        return {"message": f"Task {task_id} deleted successfully"}
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

@app.patch("/api/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(task_id: int):
    """Toggle task completion status."""
    try:
        task = manager.toggle_complete(task_id)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""Test cases for task API endpoints."""

import pytest


@pytest.mark.asyncio
class TestTaskEndpoints:
    """Test suite for task CRUD operations."""

    async def test_create_task_success(self, async_client, auth_headers, test_user_id):
        """Test creating a new task successfully."""
        response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Test Task", "description": "Test description"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test description"
        assert data["completed"] is False
        assert data["user_id"] == test_user_id
        assert "id" in data
        assert "uuid" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_task_minimal(self, async_client, auth_headers, test_user_id):
        """Test creating a task with only required fields."""
        response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Minimal Task"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None
        assert data["completed"] is False

    async def test_create_task_empty_title(self, async_client, auth_headers, test_user_id):
        """Test creating a task with empty title fails."""
        response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": ""},
            headers=auth_headers,
        )

        assert response.status_code == 422  # Validation error

    async def test_list_tasks_empty(self, async_client, auth_headers, test_user_id):
        """Test listing tasks when no tasks exist."""
        response = await async_client.get(
            f"/api/{test_user_id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert isinstance(data["tasks"], list)
        assert len(data["tasks"]) == 0
        assert data["total"] == 0

    async def test_list_tasks_with_data(self, async_client, auth_headers, test_user_id):
        """Test listing tasks with existing tasks."""
        # Create a task first
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
        assert data["total"] > 0
        assert isinstance(data["tasks"], list)

    async def test_get_task_success(self, async_client, auth_headers, test_user_id):
        """Test getting a specific task successfully."""
        # Create a task first
        create_response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Get Test Task"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = await async_client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Get Test Task"

    async def test_get_task_not_found(self, async_client, auth_headers, test_user_id):
        """Test getting a non-existent task returns 404."""
        response = await async_client.get(
            f"/api/{test_user_id}/tasks/999999",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_update_task_success(self, async_client, auth_headers, test_user_id):
        """Test updating a task successfully."""
        # Create a task first
        create_response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Original Title", "description": "Original Description"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Update the task
        response = await async_client.put(
            f"/api/{test_user_id}/tasks/{task_id}",
            json={"title": "Updated Title", "completed": True},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["completed"] is True
        assert data["description"] == "Original Description"  # Unchanged

    async def test_update_task_not_found(self, async_client, auth_headers, test_user_id):
        """Test updating a non-existent task returns 404."""
        response = await async_client.put(
            f"/api/{test_user_id}/tasks/999999",
            json={"title": "Updated Title"},
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_delete_task_success(self, async_client, auth_headers, test_user_id):
        """Test deleting a task successfully."""
        # Create a task first
        create_response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Task to Delete"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Delete the task
        response = await async_client.delete(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers,
        )

        assert response.status_code == 204

        # Verify it's deleted
        get_response = await async_client.get(
            f"/api/{test_user_id}/tasks/{task_id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404

    async def test_delete_task_not_found(self, async_client, auth_headers, test_user_id):
        """Test deleting a non-existent task returns 404."""
        response = await async_client.delete(
            f"/api/{test_user_id}/tasks/999999",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_toggle_complete_success(self, async_client, auth_headers, test_user_id):
        """Test toggling task completion status successfully."""
        # Create a task (defaults to incomplete)
        create_response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "Toggle Test Task"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]
        assert create_response.json()["completed"] is False

        # Toggle to complete
        response = await async_client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

        # Toggle back to incomplete
        response = await async_client.patch(
            f"/api/{test_user_id}/tasks/{task_id}/complete",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False

    async def test_toggle_complete_not_found(self, async_client, auth_headers, test_user_id):
        """Test toggling completion on non-existent task returns 404."""
        response = await async_client.patch(
            f"/api/{test_user_id}/tasks/999999/complete",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_user_isolation_get(self, async_client, auth_headers, test_user_id, another_user_headers, another_user_id):
        """Test user isolation - cannot access another user's task."""
        # Create task as user A
        create_response = await async_client.post(
            f"/api/{test_user_id}/tasks",
            json={"title": "User A Task"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Try to access as user B
        response = await async_client.get(
            f"/api/{another_user_id}/tasks/{task_id}",
            headers=another_user_headers,
        )

        assert response.status_code == 403  # or 404 depending on implementation

    async def test_user_isolation_list(self, async_client, auth_headers, test_user_id, another_user_id):
        """Test user isolation - can only list own tasks."""
        response = await async_client.get(
            f"/api/{another_user_id}/tasks",
            headers=auth_headers,  # auth_headers has test_user_id
        )

        # Should fail if trying to list another user's tasks with wrong auth
        # Implementation may vary: 403 forbidden vs 404 not found
        assert response.status_code in [403, 404]

    async def test_no_auth_header(self, async_client, test_user_id):
        """Test that requests without auth header are rejected."""
        response = await async_client.get(f"/api/{test_user_id}/tasks")

        assert response.status_code == 403  # Missing credentials

    async def test_invalid_auth_token(self, async_client, invalid_auth_headers, test_user_id):
        """Test that requests with invalid token are rejected."""
        response = await async_client.get(
            f"/api/{test_user_id}/tasks",
            headers=invalid_auth_headers,
        )

        assert response.status_code == 401  # Unauthorized

    async def test_pagination(self, async_client, auth_headers, test_user_id):
        """Test task listing pagination."""
        # Create multiple tasks
        for i in range(5):
            await async_client.post(
                f"/api/{test_user_id}/tasks",
                json={"title": f"Task {i}"},
                headers=auth_headers,
            )

        # Get first page (limit=2)
        response = await async_client.get(
            f"/api/{test_user_id}/tasks?skip=0&limit=2",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["total"] == 5

        # Get second page
        response = await async_client.get(
            f"/api/{test_user_id}/tasks?skip=2&limit=2",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2

    async def test_health_check(self, async_client):
        """Test health check endpoint."""
        response = await async_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_root_endpoint(self, async_client):
        """Test root endpoint."""
        response = await async_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

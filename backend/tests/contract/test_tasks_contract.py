"""
Contract tests for task endpoints.

Validates that API responses match OpenAPI specification.
"""

import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, user_data: dict) -> str:
    """Helper to register user and get auth token."""
    response = await client.post("/auth/register", json=user_data)
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_task_contract(client: AsyncClient, test_user_data: dict):
    """Test POST /tasks endpoint contract."""
    token = await get_auth_token(client, test_user_data)

    response = await client.post(
        "/tasks",
        json={"title": "Buy groceries", "description": "Milk, eggs, bread"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()

    # Validate response structure
    assert "id" in data
    assert "title" in data
    assert "description" in data
    assert "completed" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data

    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_list_tasks_contract(client: AsyncClient, test_user_data: dict):
    """Test GET /tasks endpoint contract."""
    token = await get_auth_token(client, test_user_data)

    # Create a task first
    await client.post(
        "/tasks",
        json={"title": "Test task"},
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    # Validate first task structure
    task = data[0]
    assert "id" in task
    assert "title" in task
    assert "completed" in task
    assert "user_id" in task


@pytest.mark.asyncio
async def test_get_task_contract(client: AsyncClient, test_user_data: dict):
    """Test GET /tasks/{task_id} endpoint contract."""
    token = await get_auth_token(client, test_user_data)

    # Create a task
    create_response = await client.post(
        "/tasks",
        json={"title": "Test task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Get the task
    response = await client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert "title" in data
    assert "completed" in data


@pytest.mark.asyncio
async def test_update_task_contract(client: AsyncClient, test_user_data: dict):
    """Test PUT /tasks/{task_id} endpoint contract."""
    token = await get_auth_token(client, test_user_data)

    # Create a task
    create_response = await client.post(
        "/tasks",
        json={"title": "Original title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Update the task
    response = await client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated title", "completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Updated title"
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_delete_task_contract(client: AsyncClient, test_user_data: dict):
    """Test DELETE /tasks/{task_id} endpoint contract."""
    token = await get_auth_token(client, test_user_data)

    # Create a task
    create_response = await client.post(
        "/tasks",
        json={"title": "To be deleted"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = await client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_toggle_task_contract(client: AsyncClient, test_user_data: dict):
    """Test POST /tasks/{task_id}/toggle endpoint contract."""
    token = await get_auth_token(client, test_user_data)

    # Create a task
    create_response = await client.post(
        "/tasks",
        json={"title": "To be toggled"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Toggle the task
    response = await client.post(
        f"/tasks/{task_id}/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["completed"] is True  # Should be toggled to true

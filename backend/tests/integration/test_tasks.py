"""
Integration tests for task operations.

Tests complete task CRUD flows and data isolation.
"""

import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, user_data: dict) -> str:
    """Helper to register user and get auth token."""
    response = await client.post("/auth/register", json=user_data)
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_task_creation(client: AsyncClient, test_user_data: dict):
    """Test task creation flow."""
    token = await get_auth_token(client, test_user_data)

    response = await client.post(
        "/tasks",
        json={"title": "Buy groceries", "description": "Milk, eggs, bread"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_task_update(client: AsyncClient, test_user_data: dict):
    """Test task update flow."""
    token = await get_auth_token(client, test_user_data)

    # Create task
    create_response = await client.post(
        "/tasks",
        json={"title": "Original"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Update task
    update_response = await client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated", "description": "New description"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert update_response.status_code == 200
    data = update_response.json()

    assert data["title"] == "Updated"
    assert data["description"] == "New description"


@pytest.mark.asyncio
async def test_task_deletion(client: AsyncClient, test_user_data: dict):
    """Test task deletion flow."""
    token = await get_auth_token(client, test_user_data)

    # Create task
    create_response = await client.post(
        "/tasks",
        json={"title": "To delete"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Delete task
    delete_response = await client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 204

    # Verify task is deleted
    get_response = await client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_data_isolation(client: AsyncClient, test_user_data: dict, test_user_data_2: dict):
    """
    Test that users cannot access each other's tasks.

    Critical security test for multi-tenancy.
    """
    # User 1 creates a task
    token1 = await get_auth_token(client, test_user_data)
    create_response = await client.post(
        "/tasks",
        json={"title": "User 1 task"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    task_id = create_response.json()["id"]

    # User 2 tries to access User 1's task
    token2 = await get_auth_token(client, test_user_data_2)
    get_response = await client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    # Should return 403 Forbidden
    assert get_response.status_code == 403

    # User 2 should not see User 1's task in their list
    list_response = await client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token2}"}
    )

    tasks = list_response.json()
    task_ids = [t["id"] for t in tasks]
    assert task_id not in task_ids


@pytest.mark.asyncio
async def test_task_validation_empty_title(client: AsyncClient, test_user_data: dict):
    """Test that empty title is rejected."""
    token = await get_auth_token(client, test_user_data)

    response = await client.post(
        "/tasks",
        json={"title": "   "},  # Only whitespace
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_toggle(client: AsyncClient, test_user_data: dict):
    """Test task completion toggle."""
    token = await get_auth_token(client, test_user_data)

    # Create task
    create_response = await client.post(
        "/tasks",
        json={"title": "To toggle"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Toggle to completed
    toggle_response1 = await client.post(
        f"/tasks/{task_id}/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert toggle_response1.status_code == 200
    assert toggle_response1.json()["completed"] is True

    # Toggle back to incomplete
    toggle_response2 = await client.post(
        f"/tasks/{task_id}/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert toggle_response2.status_code == 200
    assert toggle_response2.json()["completed"] is False


@pytest.mark.asyncio
async def test_task_list_retrieval(client: AsyncClient, test_user_data: dict):
    """Test retrieving task list."""
    token = await get_auth_token(client, test_user_data)

    # Create multiple tasks
    await client.post(
        "/tasks",
        json={"title": "Task 1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    await client.post(
        "/tasks",
        json={"title": "Task 2"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get task list
    response = await client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    tasks = response.json()

    assert len(tasks) >= 2
    titles = [t["title"] for t in tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles


@pytest.mark.asyncio
async def test_empty_task_list(client: AsyncClient, test_user_data: dict):
    """Test empty task list for new user."""
    token = await get_auth_token(client, test_user_data)

    response = await client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    tasks = response.json()

    assert isinstance(tasks, list)
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_status_persistence(client: AsyncClient, test_user_data: dict):
    """Test that task status persists correctly."""
    token = await get_auth_token(client, test_user_data)

    # Create and toggle task
    create_response = await client.post(
        "/tasks",
        json={"title": "Test persistence"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    await client.post(
        f"/tasks/{task_id}/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Retrieve task and verify status persisted
    get_response = await client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.json()["completed"] is True

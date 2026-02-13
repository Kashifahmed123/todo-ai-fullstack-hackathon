"""
Contract tests for authentication endpoints.

Validates that API responses match OpenAPI specification.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_contract(client: AsyncClient, test_user_data: dict):
    """
    Test /auth/register endpoint contract.

    Validates:
    - Response status code 201
    - Response contains access_token and token_type
    - token_type is "bearer"
    """
    response = await client.post("/auth/register", json=test_user_data)

    assert response.status_code == 201
    data = response.json()

    # Validate response structure
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_login_contract(client: AsyncClient, test_user_data: dict):
    """
    Test /auth/login endpoint contract.

    Validates:
    - Response status code 200
    - Response contains access_token and token_type
    - token_type is "bearer"
    """
    # First register the user
    await client.post("/auth/register", json=test_user_data)

    # Then login
    response = await client.post("/auth/login", json=test_user_data)

    assert response.status_code == 200
    data = response.json()

    # Validate response structure
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_get_me_contract(client: AsyncClient, test_user_data: dict):
    """
    Test /auth/me endpoint contract.

    Validates:
    - Response status code 200
    - Response contains id, email, created_at
    - No password in response
    """
    # Register and get token
    register_response = await client.post("/auth/register", json=test_user_data)
    token = register_response.json()["access_token"]

    # Get current user
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    # Validate response structure
    assert "id" in data
    assert "email" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data

    # Validate data types
    assert isinstance(data["id"], int)
    assert isinstance(data["email"], str)
    assert isinstance(data["created_at"], str)
    assert data["email"] == test_user_data["email"]


@pytest.mark.asyncio
async def test_register_duplicate_email_contract(client: AsyncClient, test_user_data: dict):
    """
    Test /auth/register with duplicate email returns 409.
    """
    # Register first time
    await client.post("/auth/register", json=test_user_data)

    # Try to register again with same email
    response = await client.post("/auth/register", json=test_user_data)

    assert response.status_code == 409
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials_contract(client: AsyncClient, test_user_data: dict):
    """
    Test /auth/login with invalid credentials returns 401.
    """
    response = await client.post("/auth/login", json={
        "email": test_user_data["email"],
        "password": "WrongPassword123"
    })

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_get_me_unauthorized_contract(client: AsyncClient):
    """
    Test /auth/me without token returns 401.
    """
    response = await client.get("/auth/me")

    assert response.status_code == 401  # HTTPBearer returns 401 for missing auth

"""
Integration tests for authentication flows.

Tests complete user registration, login, and authentication flows.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_registration_flow(client: AsyncClient, test_user_data: dict):
    """
    Test complete user registration flow.

    Steps:
    1. Register new user
    2. Verify token is returned
    3. Use token to access protected endpoint
    """
    # Register user
    response = await client.post("/auth/register", json=test_user_data)

    assert response.status_code == 201
    data = response.json()
    token = data["access_token"]

    # Verify token works
    me_response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["email"] == test_user_data["email"]


@pytest.mark.asyncio
async def test_user_login_flow(client: AsyncClient, test_user_data: dict):
    """
    Test complete user login flow.

    Steps:
    1. Register user
    2. Login with same credentials
    3. Verify new token works
    """
    # Register user
    await client.post("/auth/register", json=test_user_data)

    # Login
    login_response = await client.post("/auth/login", json=test_user_data)

    assert login_response.status_code == 200
    data = login_response.json()
    token = data["access_token"]

    # Verify token works
    me_response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["email"] == test_user_data["email"]


@pytest.mark.asyncio
async def test_duplicate_email_rejection(client: AsyncClient, test_user_data: dict):
    """
    Test that duplicate email registration is rejected.

    Steps:
    1. Register user
    2. Try to register again with same email
    3. Verify 409 Conflict error
    """
    # First registration
    response1 = await client.post("/auth/register", json=test_user_data)
    assert response1.status_code == 201

    # Second registration with same email
    response2 = await client.post("/auth/register", json=test_user_data)
    assert response2.status_code == 409

    error_data = response2.json()
    assert "already registered" in error_data["detail"].lower()


@pytest.mark.asyncio
async def test_invalid_credentials(client: AsyncClient, test_user_data: dict):
    """
    Test that invalid credentials are rejected.

    Steps:
    1. Register user
    2. Try to login with wrong password
    3. Verify 401 Unauthorized error
    """
    # Register user
    await client.post("/auth/register", json=test_user_data)

    # Try to login with wrong password
    response = await client.post("/auth/login", json={
        "email": test_user_data["email"],
        "password": "WrongPassword123"
    })

    assert response.status_code == 401
    error_data = response.json()
    assert "invalid" in error_data["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """
    Test that login with non-existent user is rejected.
    """
    response = await client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "SomePassword123"
    })

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    """
    Test that protected endpoints require authentication.
    """
    response = await client.get("/auth/me")

    # Should return 401 (Unauthorized) when no auth provided
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token(client: AsyncClient):
    """
    Test that protected endpoints reject invalid tokens.
    """
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token_here"}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_password_validation(client: AsyncClient):
    """
    Test password strength validation.

    Password must contain:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    # Test too short
    response1 = await client.post("/auth/register", json={
        "email": "test1@example.com",
        "password": "Short1"
    })
    assert response1.status_code == 422

    # Test no uppercase
    response2 = await client.post("/auth/register", json={
        "email": "test2@example.com",
        "password": "nouppercase123"
    })
    assert response2.status_code == 422

    # Test no lowercase
    response3 = await client.post("/auth/register", json={
        "email": "test3@example.com",
        "password": "NOLOWERCASE123"
    })
    assert response3.status_code == 422

    # Test no digit
    response4 = await client.post("/auth/register", json={
        "email": "test4@example.com",
        "password": "NoDigitHere"
    })
    assert response4.status_code == 422

    # Test valid password
    response5 = await client.post("/auth/register", json={
        "email": "test5@example.com",
        "password": "ValidPass123"
    })
    assert response5.status_code == 201


@pytest.mark.asyncio
async def test_email_validation(client: AsyncClient):
    """
    Test email format validation.
    """
    # Invalid email format
    response = await client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "ValidPass123"
    })

    assert response.status_code == 422

"""
Authentication API endpoints.

Provides user registration, login, and profile retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..core.database import get_session
from ..core.security import hash_password, verify_password, create_access_token
from ..models.user import User
from ..schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from ..api.deps import get_current_user_id


router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user.

    Creates a new user account with email and password.
    Returns JWT token for immediate authentication.

    Args:
        user_data: User registration data (email, password)
        session: Database session

    Returns:
        JWT access token

    Raises:
        HTTPException 409: Email already registered
        HTTPException 400: Invalid input data
    """
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id)})

    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    """
    Login user.

    Authenticates user with email and password.
    Returns JWT token on success.

    Args:
        user_data: User login credentials (email, password)
        session: Database session

    Returns:
        JWT access token

    Raises:
        HTTPException 401: Invalid credentials
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Get current user profile.

    Retrieves authenticated user's profile information.

    Args:
        user_id: Current user ID from JWT token
        session: Database session

    Returns:
        User profile (id, email, created_at)

    Raises:
        HTTPException 404: User not found
    """
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

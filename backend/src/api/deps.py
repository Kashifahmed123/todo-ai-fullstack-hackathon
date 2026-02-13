"""
FastAPI dependencies for database sessions and authentication.

Provides reusable dependencies for:
- Database session management
- JWT token verification
- Current user extraction
"""

from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_session
from ..core.security import verify_token


# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> int:
    """
    Extract and verify user ID from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        User ID extracted from token

    Raises:
        HTTPException: If token is invalid or missing user ID

    Example:
        @app.get("/protected")
        async def protected_route(user_id: int = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

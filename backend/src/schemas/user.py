"""
User request/response schemas.

Pydantic models for user-related API operations.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re


class UserRegister(BaseModel):
    """Schema for user registration request."""

    email: EmailStr = Field(..., max_length=255, description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password (min 8 chars, max 72 chars, must contain uppercase, lowercase, digit)"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength.
        Must contain at least one uppercase, one lowercase, and one digit.
        """
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "MyPassword123"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "MyPassword123"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""

    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2026-02-10T14:30:00Z"
            }
        }


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

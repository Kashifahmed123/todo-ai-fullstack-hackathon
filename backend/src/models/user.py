"""
User database model.

SQLModel for User entity with email and password authentication.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """
    User model for authentication and task ownership.

    Attributes:
        id: Primary key
        email: Unique email address (login identifier)
        hashed_password: Bcrypt-hashed password
        created_at: Account creation timestamp
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2026-02-10T14:30:00Z"
            }
        }

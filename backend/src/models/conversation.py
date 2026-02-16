"""
Conversation database model.

SQLModel for Conversation entity representing chat sessions.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Conversation(SQLModel, table=True):
    """
    Conversation model for chat sessions.

    Attributes:
        id: Primary key
        user_id: Foreign key to User (owner)
        created_at: Conversation creation timestamp
        updated_at: Last message timestamp
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "created_at": "2026-02-13T16:00:00Z",
                "updated_at": "2026-02-13T16:05:00Z"
            }
        }

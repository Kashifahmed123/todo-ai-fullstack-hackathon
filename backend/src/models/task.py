"""
Task database model.

SQLModel for Task entity with user ownership and completion tracking.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task model for todo items.

    Attributes:
        id: Primary key
        title: Task title (required, 1-200 chars)
        description: Optional detailed description (max 5000 chars)
        completed: Completion status (default: False)
        user_id: Foreign key to User (owner)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "user_id": 1,
                "created_at": "2026-02-10T14:30:00Z",
                "updated_at": "2026-02-10T14:30:00Z"
            }
        }

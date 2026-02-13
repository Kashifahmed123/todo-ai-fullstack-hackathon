"""
Task request/response schemas.

Pydantic models for task-related API operations.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for task creation request."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional task description (max 5000 characters)"
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, v: str) -> str:
        """Validate that title is not only whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for task update request."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Updated task description"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status"
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not only whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "description": "Updated description",
                "completed": True
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
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

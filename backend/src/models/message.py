"""
Message database model.

SQLModel for Message entity representing individual chat messages.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Message(SQLModel, table=True):
    """
    Message model for chat messages within conversations.

    Attributes:
        id: Primary key
        conversation_id: Foreign key to Conversation
        user_id: Foreign key to User (for user isolation)
        role: Message role ('user' or 'assistant')
        content: Message text content
        created_at: Message creation timestamp
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "conversation_id": 1,
                "user_id": 1,
                "role": "user",
                "content": "Add a task to buy milk",
                "created_at": "2026-02-13T16:00:00Z"
            }
        }

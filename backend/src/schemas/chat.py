"""
Chat schemas for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, List


class ChatMessageRequest(BaseModel):
    """Request schema for chat messages."""

    message: str
    conversation_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Response schema for chat messages."""

    response: str
    conversation_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "response": "I've added 'buy milk' to your task list.",
                "conversation_id": 1
            }
        }

"""
Chat API endpoints.

Implements stateless chat endpoint that fetches history from DB
and processes messages through OpenAI Agent with MCP tools.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime
from typing import List

from ..core.database import get_session
from ..api.deps import get_current_user_id
from ..models import User, Conversation, Message
from ..schemas.chat import ChatMessageRequest, ChatMessageResponse
from ..core.mcp_tools import MCPTools

router = APIRouter(prefix="/chat", tags=["chat"])


async def get_or_create_conversation(
    session: AsyncSession,
    user_id: int,
    conversation_id: int = None
) -> Conversation:
    """
    Get existing conversation or create new one.

    Args:
        session: Database session
        user_id: User ID
        conversation_id: Optional existing conversation ID

    Returns:
        Conversation object
    """
    if conversation_id:
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(query)
        conversation = result.scalar_one_or_none()

        if conversation:
            return conversation
        # If conversation not found (e.g., database reset), create new one

    # Create new conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def fetch_conversation_history(
    session: AsyncSession,
    conversation_id: int
) -> List[Message]:
    """
    Fetch conversation history from database (stateless).

    Args:
        session: Database session
        conversation_id: Conversation ID

    Returns:
        List of messages ordered by creation time
    """
    query = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at)

    result = await session.execute(query)
    return result.scalars().all()


async def process_with_agent(
    user_message: str,
    history: List[Message],
    session: AsyncSession,
    user_id: int
) -> str:
    """
    Process message with OpenAI Agent and MCP tools.

    This is a placeholder implementation with basic context tracking.
    In production, this would use OpenAI Agents SDK.

    Args:
        user_message: User's message
        history: Conversation history
        session: Database session for tool execution
        user_id: User ID for tool isolation

    Returns:
        Agent response string
    """
    message_lower = user_message.lower()

    # Check conversation context from last assistant message
    last_assistant_message = None
    if len(history) > 0:
        for msg in reversed(history):
            if msg.role == "assistant":
                last_assistant_message = msg.content
                break

    # Context-aware responses
    if last_assistant_message:
        # If AI asked "What task would you like to add?", treat current message as task title
        if "what task would you like to add" in last_assistant_message.lower():
            title = user_message.strip()
            result = await MCPTools.add_task(session, user_id, title)
            if result["success"]:
                return f"I've added '{title}' to your task list."
            return "Sorry, I couldn't add that task."

        # If AI asked "Which task...", treat current message as task number
        if "which task" in last_assistant_message.lower():
            words = user_message.split()
            task_id = None
            for word in words:
                if word.isdigit():
                    task_id = int(word)
                    break

            if not task_id:
                return "Please provide a task number."

            # Determine action from previous context
            if "complete" in last_assistant_message.lower() or "mark" in last_assistant_message.lower():
                result = await MCPTools.complete_task(session, user_id, task_id)
                if result["success"]:
                    return f"Great! I've marked task {task_id} as complete."
                return result.get("error", "Sorry, I couldn't complete that task.")

            elif "delete" in last_assistant_message.lower() or "remove" in last_assistant_message.lower():
                result = await MCPTools.delete_task(session, user_id, task_id)
                if result["success"]:
                    return f"I've deleted task {task_id} from your list."
                return result.get("error", "Sorry, I couldn't delete that task.")

    # Direct command processing
    if "add" in message_lower and "task" in message_lower:
        # Extract task title (simplified)
        title = user_message.replace("add", "").replace("Add", "").replace("task", "").replace("Task", "").replace("a", "").replace("to", "").strip()
        if not title or len(title) < 2:
            return "What task would you like to add?"

        result = await MCPTools.add_task(session, user_id, title)
        if result["success"]:
            return f"I've added '{title}' to your task list."
        return "Sorry, I couldn't add that task."

    elif "list" in message_lower or "show" in message_lower or "what" in message_lower:
        result = await MCPTools.list_tasks(session, user_id)
        if result["success"]:
            if result["count"] == 0:
                return "Your task list is empty."
            tasks_text = "\n".join([
                f"Task {task['id']}: {task['title']} {'✓' if task['completed'] else '○'}"
                for task in result["tasks"]
            ])
            return f"Here are your tasks:\n{tasks_text}"
        return "Sorry, I couldn't retrieve your tasks."

    elif "complete" in message_lower or "done" in message_lower or "mark" in message_lower:
        # Extract task ID (simplified)
        words = user_message.split()
        task_id = None
        for word in words:
            if word.isdigit():
                task_id = int(word)
                break

        if not task_id:
            return "Which task would you like to mark as complete? Please provide the task number."

        result = await MCPTools.complete_task(session, user_id, task_id)
        if result["success"]:
            return f"Great! I've marked task {task_id} as complete."
        return result.get("error", "Sorry, I couldn't complete that task.")

    elif "delete" in message_lower or "remove" in message_lower:
        # Extract task ID (simplified)
        words = user_message.split()
        task_id = None
        for word in words:
            if word.isdigit():
                task_id = int(word)
                break

        if not task_id:
            return "Which task would you like to delete? Please provide the task number."

        result = await MCPTools.delete_task(session, user_id, task_id)
        if result["success"]:
            return f"I've deleted task {task_id} from your list."
        return result.get("error", "Sorry, I couldn't delete that task.")

    else:
        return "I can help you manage your tasks. Try saying 'add a task', 'show my tasks', 'complete task 1', or 'delete task 2'."


@router.post("/", response_model=ChatMessageResponse)
async def chat(
    request: ChatMessageRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Stateless chat endpoint.

    Process flow:
    1. Get or create conversation
    2. Fetch conversation history from DB (stateless)
    3. Process message with OpenAI Agent + MCP tools
    4. Save user message and agent response to DB
    5. Return response

    Args:
        request: Chat message request
        current_user_id: Authenticated user ID
        session: Database session

    Returns:
        Chat response with conversation ID
    """
    # Step 1: Get or create conversation
    conversation = await get_or_create_conversation(
        session,
        current_user_id,
        request.conversation_id
    )

    # Step 2: Fetch history (stateless - no memory in RAM)
    history = await fetch_conversation_history(session, conversation.id)

    # Step 3: Save user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=current_user_id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    await session.commit()

    # Step 4: Process with agent
    agent_response = await process_with_agent(
        request.message,
        history,
        session,
        current_user_id
    )

    # Step 5: Save agent response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=current_user_id,
        role="assistant",
        content=agent_response
    )
    session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    await session.commit()

    return ChatMessageResponse(
        response=agent_response,
        conversation_id=conversation.id
    )

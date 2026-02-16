"""
MCP Tools for Task Management.

Implements Model Context Protocol tools for natural language task operations.
All tools enforce user_id isolation from JWT authentication.
"""

from typing import Dict, Any, List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Task


class MCPTools:
    """
    MCP tool implementations for task management.

    All methods require user_id for isolation and session for database access.
    """

    @staticmethod
    async def add_task(
        session: AsyncSession,
        user_id: int,
        title: str,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Add a new task for the authenticated user.

        Args:
            session: Database session
            user_id: Authenticated user ID (from JWT)
            title: Task title
            description: Optional task description

        Returns:
            Dict with task details
        """
        task = Task(
            title=title,
            description=description,
            user_id=user_id,
            completed=False
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
        }

    @staticmethod
    async def list_tasks(
        session: AsyncSession,
        user_id: int,
        completed: bool = None
    ) -> Dict[str, Any]:
        """
        List all tasks for the authenticated user.

        Args:
            session: Database session
            user_id: Authenticated user ID (from JWT)
            completed: Optional filter by completion status

        Returns:
            Dict with list of tasks
        """
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        result = await session.execute(query)
        tasks = result.scalars().all()

        return {
            "success": True,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
                for task in tasks
            ],
            "count": len(tasks)
        }

    @staticmethod
    async def complete_task(
        session: AsyncSession,
        user_id: int,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            session: Database session
            user_id: Authenticated user ID (from JWT)
            task_id: Task ID to complete

        Returns:
            Dict with success status
        """
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "error": f"Task {task_id} not found or access denied"
            }

        task.completed = True
        await session.commit()

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
        }

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        user_id: int,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            session: Database session
            user_id: Authenticated user ID (from JWT)
            task_id: Task ID to delete

        Returns:
            Dict with success status
        """
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "error": f"Task {task_id} not found or access denied"
            }

        await session.delete(task)
        await session.commit()

        return {
            "success": True,
            "message": f"Task {task_id} deleted successfully"
        }

    @staticmethod
    async def update_task(
        session: AsyncSession,
        user_id: int,
        task_id: int,
        title: str = None,
        description: str = None,
        completed: bool = None
    ) -> Dict[str, Any]:
        """
        Update a task's properties.

        Args:
            session: Database session
            user_id: Authenticated user ID (from JWT)
            task_id: Task ID to update
            title: Optional new title
            description: Optional new description
            completed: Optional new completion status

        Returns:
            Dict with updated task details
        """
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "error": f"Task {task_id} not found or access denied"
            }

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
        }

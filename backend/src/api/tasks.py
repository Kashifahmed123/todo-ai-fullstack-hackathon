"""
Task API endpoints.

Provides CRUD operations for tasks with user ownership enforcement.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime

from ..core.database import get_session
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..api.deps import get_current_user_id


router = APIRouter()


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    List all tasks for authenticated user.

    Returns all tasks owned by the current user.

    Args:
        user_id: Current user ID from JWT token
        session: Database session

    Returns:
        List of tasks
    """
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task.

    Creates a task owned by the authenticated user.

    Args:
        task_data: Task creation data
        user_id: Current user ID from JWT token
        session: Database session

    Returns:
        Created task

    Raises:
        HTTPException 400: Invalid input data
    """
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific task.

    Retrieves a task by ID. User must own the task.

    Args:
        task_id: Task ID
        user_id: Current user ID from JWT token
        session: Database session

    Returns:
        Task details

    Raises:
        HTTPException 404: Task not found
        HTTPException 403: Task belongs to another user
    """
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a task.

    Updates task title, description, or completion status.
    User must own the task.

    Args:
        task_id: Task ID
        task_data: Task update data
        user_id: Current user ID from JWT token
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException 404: Task not found
        HTTPException 403: Task belongs to another user
        HTTPException 400: Invalid input data
    """
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a task.

    Permanently deletes a task. User must own the task.

    Args:
        task_id: Task ID
        user_id: Current user ID from JWT token
        session: Database session

    Raises:
        HTTPException 404: Task not found
        HTTPException 403: Task belongs to another user
    """
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    await session.delete(task)
    await session.commit()


@router.post("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle task completion status.

    Toggles between completed and incomplete.
    User must own the task.

    Args:
        task_id: Task ID
        user_id: Current user ID from JWT token
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException 404: Task not found
        HTTPException 403: Task belongs to another user
    """
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task

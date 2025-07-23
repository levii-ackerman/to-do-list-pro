from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models import Task, GroupTask, GroupTaskAssignment
from schemas import TaskCreate, TaskRead, TaskUpdate, GroupTaskRead
from typing import List

async def create_task(user_id: int, task_data: TaskCreate, session: AsyncSession) -> Task:
    new_task = Task(**task_data.model_dump(), user_id = user_id)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

async def get_user_tasks(user_id: int, session: AsyncSession) -> List[Task]:
    tasks = await session.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return tasks.scalars().all()

async def get_task_by_id(task_id: int, user_id: int, session: AsyncSession) -> Task:
    result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
    return result.scalar_one_or_none()

async def update_task(task_id: int, user_id: int, task_data: TaskUpdate, session: AsyncSession) -> Task:
    task = await get_task_by_id(task_id, user_id, session)
    if not task:
        return None
    
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(task_id: int, user_id: int, session: AsyncSession):
    task = await get_task_by_id(task_id, user_id, session)
    if not task:
        return None
    await session.delete(task)
    await session.commit()
    return True

async def my_group_task(user_id: int, session: AsyncSession) -> list[GroupTaskRead]:
    stmt = select(GroupTask).join(GroupTaskAssignment).where(GroupTaskAssignment.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
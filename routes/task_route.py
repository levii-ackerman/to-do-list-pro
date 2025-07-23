from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services import task
from core.models import User
from schemas import TaskCreate, TaskRead, TaskUpdate
from auth.check_user import get_current_user
from core.database import get_async_session

task_router = APIRouter(
    prefix='/task'
)

@task_router.post('/make')
async def make_task(task_data: TaskCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return await task.create_task(current_user.id, task_data, session)

@task_router.get('/tasks')
async def get_user_task(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return await task.get_user_tasks(current_user.id, session)

@task_router.get('/{task_id}/task', response_model=TaskRead)
async def task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    cr_task =  await task.get_task_by_id(task_id, current_user.id, session)
    if not cr_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='task not found'
        )
    return cr_task

@task_router.put('/{task_id}/update')
async def task_update(task_id: int, task_data: TaskUpdate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    upd_task = await task.update_task(task_id, current_user.id, task_data, session)
    if not upd_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    return upd_task

@task_router.delete('/{task_id}/delete')
async def task_delete(task_id: int, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    dl_task = await task.delete_task(task_id, current_user.id, session)
    if not dl_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    return True

@task_router.get('/my_group_tasks')
async def get_my_group_task(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await task.my_group_task(current_user.id, session)
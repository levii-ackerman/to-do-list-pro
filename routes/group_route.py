from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from services import group
from core.models import Group, User
from core.database import get_async_session
from auth.check_user import get_current_user
from schemas import GroupCreate, GroupMemberAdd, GroupTaskAdd, GroupTaskAssignmentCreate, GroupMemberRemove

from sqlalchemy.ext.asyncio import AsyncSession

group_router = APIRouter(
    prefix='/group'
)

@group_router.post('/make')
async def make_group(group_data: GroupCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await group.create_group(owner_id=current_user.id, group_data=group_data, session=session)

@group_router.post('/{group_id}/add_member')
async def add_member(group_id: int, user_data: GroupMemberAdd, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await group.add_member_group(group_id=group_id, user_data=user_data, session=session)

@group_router.get('/{group_id}/members')
async def get_members(group_id: int, session: AsyncSession = Depends(get_async_session)):
    return await group.get_group_members(group_id=group_id, session=session)

@group_router.post('/{group_id}/add_task')
async def add_task_group(group_id: int, group_data: GroupTaskAdd, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await group.create_group_task(group_id=group_id, group_data=group_data, session=session)

@group_router.post('/{group_id}/assign_task')
async def assign_task_user(user_data: GroupTaskAssignmentCreate, session: AsyncSession = Depends(get_async_session)):
    return await group.assign_task_to_user(user_data=user_data, session=session)

@group_router.delete('/{group_id}/member_remove')
async def remove_member(group_data: GroupMemberRemove, session: AsyncSession = Depends(get_async_session)):
    return await group.remove_group_member(group_data=group_data, session=session)
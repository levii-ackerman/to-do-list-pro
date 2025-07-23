from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from sqlalchemy.exc import IntegrityError

from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder

from core.models import Group, GroupMember, GroupTask, GroupTaskAssignment
from schemas import GroupCreate, GroupMemberAdd, GroupTaskAdd, GroupTaskAssignmentCreate, GroupMemberRemove
from typing import List

async def create_group(owner_id: int, group_data: GroupCreate, session: AsyncSession) -> Group:
    new_group = Group(name=group_data.name, owner_id = owner_id)
    session.add(new_group)
    await session.commit()
    await session.refresh(new_group)

    response_model = {
        'success': True,
        'message': 'Group successfully created',
        'code': 200,
        'data': {
            'group_id': new_group.id,
            'group_name': new_group.name
        }
    }

    return jsonable_encoder(response_model)

async def add_member_group(group_id: int, user_data: GroupMemberAdd, session: AsyncSession):
    stmt = insert(GroupMember).values(group_id = group_id, user_id = user_data.user_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User allaqachon guruhda bor'
        )
    response_model = {
        'success': True,
        'message': 'User successfully added',
        'code': 200,
        'data': {
            'user_id': user_data.user_id
        }
    }

    return jsonable_encoder(response_model)
async def get_group_members(group_id: int, session: AsyncSession):
    stmt = select(GroupMember).where(GroupMember.group_id == group_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_group_task(group_id: int, group_data: GroupTaskAdd, session: AsyncSession):
    new_task = GroupTask(
        title = group_data.title,
        description = group_data.description,
        deadline = group_data.deadline
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    
    response_model = {
        'success': True,
        'message': 'Task successfully created',
        'code': 200,
        'data': {
            'task_id': new_task.id,
            'task_title': new_task.title,
            'task_deadline': new_task.deadline
        }
    }

    return jsonable_encoder(response_model)

async def assign_task_to_user(user_data: GroupTaskAssignmentCreate, session: AsyncSession):
    stmt = insert(GroupTaskAssignment).values(task_id = user_data.task_id, user_id = user_data.user_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Userga allaqachon task biriktirilgan'
        )
    response_model = {
        'success': True,
        'message': 'Task successfully assignmeted',
        'code': 200
    }
    
async def remove_group_member(group_data: GroupMemberRemove, session: AsyncSession):
    stmt = delete(GroupMember).where(GroupMember.group_id == group_data.group_id, GroupMember.user_id == group_data.user_id)
    await session.execute(stmt)
    await session.commit()

    response_model = {
        'success': True,
        'message': 'User successfully deleted',
        'code': 200,
        'data': {
            'user_id': group_data.user_id,
        }
    }

    return jsonable_encoder(response_model)
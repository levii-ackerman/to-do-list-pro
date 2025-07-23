from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from core.models import Friend
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from schemas import FriendCreate, FriendRespone

async def add_friend(user_id: int, friend_data: FriendCreate, session: AsyncSession):
    stmt = insert(Friend).values(user_id = user_id, friend_id = friend_data.friend_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Dost allaqachon qoshilgan'
        )
    response_model = {
        'success': True,
        'message': 'Friend successfully added',
        'code': 200
    }

    return jsonable_encoder(response_model)


async def get_friends(user_id: int, session: AsyncSession):
    stmt = select(Friend).where(Friend.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_friend(friend_id: int, user_id: int, session: AsyncSession):
    stmt = select(Friend).where(Friend.user_id == user_id, Friend.friend_id == friend_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def remove_friend(user_id: int, friend_id: int, session: AsyncSession):
    stmt = delete(Friend).where(Friend.user_id == user_id, Friend.friend_id == friend_id)
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dost topilmadi'
        )
    
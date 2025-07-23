from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Friend, User
from core.database import get_async_session
from schemas import FriendCreate, FriendRespone
from auth.check_user import get_current_user
from services import friend

friend_router = APIRouter(
    prefix='/friend'
)

@friend_router.post('/add_friend')
async def add_friend(friend_data: FriendCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if friend_data.friend_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Siz o'zingizni friendga qo'sha olmaysiz"
        )
    result = await friend.add_friend(current_user.id, friend_data, session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Do'st allaqachon qo'shilgan yokida xatolik mavjud"
        )
    
    response_model = {
        'success': True,
        'message': 'Friend successfully added',
        'code': 200,
        "data": {
            'friend_id': friend_data.friend_id,
        }
    }

@friend_router.get('/friends')
async def get_friends(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await friend.get_friends(current_user.id, session)

@friend_router.get('/{friend_id}/friend')
async def get_friend_by_id(friend_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await friend.get_friend(friend_id, current_user.id, session)

@friend_router.delete('/{friend_id}/remove')
async def delete_friend(friend_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await friend.remove_friend(current_user.id, friend_id, session)
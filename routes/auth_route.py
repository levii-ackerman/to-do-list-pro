from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from sqlalchemy.future import select

from schemas import UserCreate, UserLogin, Token
from services.user import get_user_by_email, craete_user, authenticate_user
from services.hashing import check_password
from core.database import get_async_session
from auth.jwt import create_access_token
from core.models import User

auth_router = APIRouter(
    prefix='/auth'
)

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await get_user_by_email(user_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This is user already exists'
        )
    user = await craete_user(user_data, session)
    
    response_model = {
        'success': True,
        'message': 'User successfully created',
        'code': 200
    }

    return jsonable_encoder(response_model)

@auth_router.post('/login')
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(
        or_(
            User.username == user_data.email_or_username,
            User.email == user_data.email_or_username
        )
    )
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    if not check_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='assword incorrect'
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type='bearer')
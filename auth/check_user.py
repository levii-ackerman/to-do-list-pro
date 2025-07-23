from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_async_session
from core.models import User
from core.configs import get_settings

oauth2_schem = OAuth2PasswordBearer(tokenUrl='login')
settings = get_settings()
async def get_current_user(session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_schem)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = (payload.get('sub'))
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Enter valid token'
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token decoding error'
        )
    
    user = await session.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user
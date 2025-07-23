from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models import User
from services.hashing import hash_password, check_password
from schemas import UserCreate, UserLogin

async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def craete_user(user: UserCreate, session: AsyncSession) -> User:
    new_user = User(
        username = user.username,
        email = user.email,
        full_name = user.full_name,
        password = hash_password(user.password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def authenticate_user(user: UserLogin, session: AsyncSession) -> User | None:
    login_user = await get_user_by_email(user.email_or_username, session)
    if not login_user:
        return None
    return login_user
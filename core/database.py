from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.configs import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
sync_engine = create_engine(settings.DATABASE_URL.replace("asyncpg", "psycopg2"))
SyncSessionLocal = sessionmaker(bind=sync_engine)

Base = declarative_base()

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
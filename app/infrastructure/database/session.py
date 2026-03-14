from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (create_async_engine, AsyncSession,
                                    async_sessionmaker)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

sync_engine = create_engine(
    settings.database_url.replace("postgresql+asyncpg://", "postgresql://"),
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    class_=Session,
)

# Асинхронный движок для asyncpg
engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True,
)
# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """Получает асинхронную сессию базы данных."""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def init_db() -> None:
    """Создаёт все таблицы в базе данных (асинхронно)."""
    from app.infrastructure.database.models import PriceRecord
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully")

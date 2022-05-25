from typing import AsyncGenerator, Tuple

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from app.config.settings import (MONGO_DB, MONGO_HOST, MONGO_PASSWORD,
                                 MONGO_PORT, MONGO_USER)


# sql
def create_engine_async_app(
        db_url: str, pool_size: int = 5, max_overflow: int = 5, pool_timeout: int = 30
) -> Tuple[AsyncEngine, AsyncSession]:
    async_engine = create_async_engine(
        db_url,
        future=True,
        echo=False,
        pool_pre_ping=True,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
    )
    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_engine, async_session  # noqa


async def get_db(request: Request) -> AsyncGenerator:
    db = request.app.state.sessionmaker()
    try:
        yield db
    except SQLAlchemyError as ex:
        await db.rollback()
        raise ex
    finally:
        await db.close()


# MongoDB

async def get_mongo_db() -> AsyncIOMotorClient:
    link = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    client = AsyncIOMotorClient(link)
    try:
        yield client
    finally:
        client.close()

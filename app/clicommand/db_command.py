import click

from app.aiembic_import import Base
from app.config.settings import SQLALCHEMY_DATABASE_URI
from app.core.db.database import create_engine_async_app
from app.core.utils.base import coro


@click.group()
def db():
    pass


@db.command()
@coro
async def create_all_table():
    engine, session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@db.command()
@coro
async def delete_all_table():
    engine, session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

import click

from app.aiembic_import import Base
from app.config.settings import SQLALCHEMY_DATABASE_URI
from app.core.db.databases import create_engine_async_app
from app.core.utils.base import coro


@click.group(help="Common commands for working with the database")
def db():
    pass


@db.command(help="Create all table in db")
@coro
async def create_all_table():
    engine, session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@db.command(help="Delete all table in db")
@coro
async def delete_all_table():
    engine, session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

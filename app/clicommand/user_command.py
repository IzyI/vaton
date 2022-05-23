import uuid

import click

from app.api.user.models import CRUDUser, CRUDUserInfo, CRUDUserRole
from app.api.user.schemas import BaseUser, BaseUserInfo, BaseUserRole
from app.config.settings import SALT, SQLALCHEMY_DATABASE_URI, USER_ROLE
from app.core.db.database import create_engine_async_app
from app.core.utils.base import coro
from app.core.utils.secur import get_password_hash


@click.group()
def user():
    pass


@user.command()
@click.option("--count", default=1, help="number of greetings")
@click.argument("name")
def hello(count, name):
    for x in range(count):
        click.echo(f"Hello {name}!")


@user.command()
@coro
@click.argument("email")
@click.argument("password")
@click.argument("role")
@click.argument("username", default=None)
async def create(email, password, role, username):
    _, async_session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with async_session() as session:  # noqa
        user_obj = await CRUDUser.create(
            session,
            BaseUser(password=get_password_hash(password, SALT), email=email),
        )
        if not username:
            username = email.split("@")[0]
        await CRUDUserInfo.create(
            session,
            BaseUserInfo(username=username, bio=str(uuid.uuid4()), id_user=user_obj.id),
        )
        await CRUDUser.pin_user_to_role(session, user_obj.id, USER_ROLE[role])
        click.echo(user_obj)


@user.command()
@click.argument("email")
@coro
async def delete(email):
    _, async_session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with async_session() as session:  # noqa
        user_obj = await CRUDUser.get_user_by_email(session, email)
        if user_obj:
            await CRUDUser.remove(session, id=user_obj.id)
            click.echo(user_obj)
        else:
            click.echo("Not found")


@user.command()
@coro
async def create_all_role():
    _, async_session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with async_session() as session:  # noqa
        # Get the last 100 UserRole
        u_r = await CRUDUserRole.get_multi(session)
        for i in u_r:
            await CRUDUserRole.remove(session, id=i.id)
        for i in USER_ROLE:
            await CRUDUserRole.create(
                session, BaseUserRole(role=i, id=int(USER_ROLE[i]))
            )

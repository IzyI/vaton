import uuid

import click

from app.api.user.dbmodel.vaton_user import VUser
from app.api.user.dbmodel.vaton_user_info import VUserInfo
from app.api.user.dbmodel.vaton_user_role import VUserRole
from app.api.user.model.m_user import ModelUser
from app.api.user.model.m_user_info import ModelUserInfo
from app.api.user.model.m_user_role import ModelUserRole
from app.api.user.schemas import BaseUser, BaseUserInfo, BaseUserRole
from app.config.settings import SALT, SQLALCHEMY_DATABASE_URI, USER_ROLE
from app.core.db.databases import create_engine_async_app
from app.core.utils.base import coro
from app.core.utils.secur import get_password_hash


@click.group(help='Common commands for working with users')
def user():
    pass


@user.command(help='Create a user')
@coro
@click.argument("email")
@click.argument("password")
@click.argument("role")
@click.argument("username", default=None)
async def create(email, password, role, username):
    _, async_session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with async_session() as session:  # noqa
        user_obj = await ModelUser(VUser).create(
            session,
            BaseUser(password=get_password_hash(password, SALT), email=email),
        )
        if not username:
            username = email.split("@")[0]
        await ModelUserInfo(VUserInfo).create(
            session,
            BaseUserInfo(username=username, bio=str(uuid.uuid4()), id_user=user_obj.id),
        )
        await ModelUser(VUser).pin_user_to_role(session, user_obj.id, USER_ROLE[role])
        click.echo(user_obj)


@user.command(help='Deleting a user by email')
@click.argument("email")
@coro
async def delete(email):
    _, async_session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with async_session() as session:  # noqa
        user_obj = await ModelUser(VUser).get_user_by_email(session, email)
        if user_obj:
            await ModelUser(VUser).remove(session, id=user_obj.id)
            click.echo(user_obj)
        else:
            click.echo("Not found")


@user.command(help='Creating basic roles  {"admin": 333, "manager": 222, "user": 111, "bot": 444}')
@coro
async def create_all_role():
    _, async_session = create_engine_async_app(SQLALCHEMY_DATABASE_URI)
    async with async_session() as session:  # noqa
        # Get the last 100 UserRole
        u_r = await ModelUserRole(VUserRole).get_multi(session)
        for i in u_r:
            await ModelUserRole(VUserRole).remove(session, id=i.id)
        for i in USER_ROLE:
            await ModelUserRole(VUserRole).create(
                session, BaseUserRole(role=i, id=int(USER_ROLE[i]))
            )

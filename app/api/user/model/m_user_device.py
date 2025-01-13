from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.user.dbmodel.vaton_user_device import VUserDevice
from app.api.user.schemas import BaseUpdateUserDevice, BaseUserDevice
from app.core.db.sqlalchemy_crud import CrudBase


class ModelUserDevice(CrudBase[VUserDevice, BaseUserDevice, BaseUpdateUserDevice]):
    def __init__(self, model: Type[VUserDevice]):
        super().__init__(model)  # noqa

    async def get_by_token(self, db: AsyncSession, token: str):
        user_role = await db.execute(
            select(self.model).filter(VUserDevice.token == token)
        )
        return user_role.scalars().first()

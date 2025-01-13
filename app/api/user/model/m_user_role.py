from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.user.dbmodel.vaton_user_role import VUserRole
from app.api.user.schemas import BaseUserRole
from app.core.db.sqlalchemy_crud import CrudBase


class ModelUserRole(CrudBase[VUserRole, BaseUserRole, BaseUserRole]):
    def __init__(self, model: Type[VUserRole]):
        super().__init__(model)  # noqa

    async def get_role(self, db: AsyncSession, role: str):
        user_role = await db.execute(select(self.model).filter(VUserRole.role == role))
        return user_role.scalars().first()

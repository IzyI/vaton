from typing import Optional, Type

from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.api.user.dbmodel.vaton_user import VUser, association_user_role
from app.api.user.schemas import BaseUser
from app.core.db.sqlalchemy_crud import CrudBase


class ModelUser(CrudBase[VUser, BaseUser, BaseUser]):
    def __init__(self, model: Type[VUser]):
        super().__init__(model)  # noqa
        self.user = None
        self.token = None

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[VUser]:
        """
        Get User model by email.
        """
        user = await db.execute(select(self.model).filter(VUser.email == email))
        self.user = user.scalars().first()
        return self.user

    async def get_user_by_email_with_device(
        self, db: AsyncSession, email: str
    ) -> Optional[VUser]:
        """
        Get User model by email.
        """
        user = await db.execute(
            select(self.model)
            .options(selectinload(self.model.devices))
            .filter(VUser.email == email)
        )
        self.user = user.scalars().first()
        return self.user

    async def authenticate_user(
        self, db: AsyncSession, email: str, password: str
    ) -> Optional[VUser]:
        """
        Get User model by email.
        """
        user = await db.execute(
            select(self.model)
            .filter(VUser.email == email)
            .filter(VUser.password == password)
        )
        self.user = user.scalars().first()
        return self.user

    async def pin_user_to_role(self, db: AsyncSession, user_id: int, role_id: int):
        await db.execute(
            insert(association_user_role).values(
                vaton_user_id=user_id, vaton_user_role_id=role_id
            )
        )
        await db.commit()

    async def unpin_user_to_role(self, db: AsyncSession, user_id, role_id):
        await db.execute(
            delete(association_user_role).values(
                vaton_user_id=user_id, vaton_user_role_id=role_id
            )
        )
        await db.commit()

from datetime import datetime
from typing import Optional, Type

from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String, Table, delete, insert)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, selectinload

from app.api.user.schemas import (BaseUpdateUserDevice, BaseUser,
                                  BaseUserDevice, BaseUserInfo, BaseUserRole)
from app.core.db.base_class import Base
from app.core.db.base_crud import CRUDBase

association_user_role = Table(
    "association_user_role",
    Base.metadata,  # type: ignore
    Column(
        "vaton_user_id",
        BigInteger,
        ForeignKey("vaton_user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "vaton_user_role_id",
        BigInteger,
        ForeignKey("vaton_user_role.id"),
        primary_key=True,
    ),
)


class VUser(Base):
    __tablename__ = "vaton_user"  # type: ignore
    __mapper_args__ = {"eager_defaults": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
    user_info = relationship(
        "VUserInfo",
        uselist=False,
        backref="vaton_user",
        lazy="joined",
        cascade="all, delete",
    )
    user_role = relationship(
        "VUserRole",
        secondary=association_user_role,
        lazy="joined",
        cascade="all, delete",
    )
    devices = relationship("VUserDevice")
    registration_time = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"User (id={self.id},email={self.email} registration_time:{self.registration_time})"


class VUserDevice(Base):
    __tablename__ = "vaton_user_device"  # type: ignore
    __mapper_args__ = {"eager_defaults": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True)
    ip = Column(String)
    type = Column(String)
    version = Column(String)
    state = Column(String)
    id_user = Column(Integer, ForeignKey("vaton_user.id", ondelete="CASCADE"))
    create_time = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"Device (id={self.id},type={self.type} create_time:{self.create_time})"


class VUserInfo(Base):
    __tablename__ = "vaton_user_info"  # type: ignore
    __mapper_args__ = {"eager_defaults": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    bio = Column(String, unique=True)
    id_user = Column(Integer, ForeignKey("vaton_user.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"User Info id={self.id} ({self.username}/{self.id_user})"


class VUserRole(Base):
    __tablename__ = "vaton_user_role"  # type: ignore
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)

    def __repr__(self):
        return f"User Role(id={self.id},role={self.role})"


class DecorCRUDUser(CRUDBase[VUser, BaseUser, BaseUser]):
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


class DecorCRUDUserRole(CRUDBase[VUserRole, BaseUserRole, BaseUserRole]):
    def __init__(self, model: Type[VUserRole]):
        super().__init__(model)  # noqa

    async def get_role(self, db: AsyncSession, role: str):
        user_role = await db.execute(select(self.model).filter(VUserRole.role == role))
        return user_role.scalars().first()


class DecorCRUDUserDevice(CRUDBase[VUserDevice, BaseUserDevice, BaseUpdateUserDevice]):
    def __init__(self, model: Type[VUserDevice]):
        super().__init__(model)  # noqa

    async def get_by_token(self, db: AsyncSession, token: str):
        user_role = await db.execute(
            select(self.model).filter(VUserDevice.token == token)
        )
        return user_role.scalars().first()


CRUDUser: DecorCRUDUser = DecorCRUDUser(VUser)
CRUDUserInfo: CRUDBase = CRUDBase[VUserInfo, BaseUserInfo, BaseUserInfo](VUserInfo)
CRUDUserRole: DecorCRUDUserRole = DecorCRUDUserRole(VUserRole)
CRUDUserDevice: DecorCRUDUserDevice = DecorCRUDUserDevice(VUserDevice)

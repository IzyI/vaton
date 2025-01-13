from datetime import datetime

from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.orm import relationship

from app.api.user.model.m_user_device import VUserDevice
from app.api.user.model.m_user_info import VUserInfo
from app.api.user.model.m_user_role import VUserRole
from app.core.db.sqlalchemy_base_class import Base

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
        VUserInfo,
        uselist=False,
        backref="vaton_user",
        lazy="joined",
        cascade="all, delete",
    )
    user_role = relationship(
        VUserRole,
        secondary=association_user_role,
        lazy="joined",
        cascade="all, delete",
    )
    devices = relationship(VUserDevice)
    registration_time = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"User (id={self.id},email={self.email} registration_time:{self.registration_time})"

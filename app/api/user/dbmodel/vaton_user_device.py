from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.core.db.sqlalchemy_base_class import Base


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

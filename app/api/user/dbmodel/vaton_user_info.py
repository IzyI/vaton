from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.db.sqlalchemy_base_class import Base


class VUserInfo(Base):
    __tablename__ = "vaton_user_info"  # type: ignore
    __mapper_args__ = {"eager_defaults": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    bio = Column(String, unique=True)
    id_user = Column(Integer, ForeignKey("vaton_user.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"User Info id={self.id} ({self.username}/{self.id_user})"

from sqlalchemy import Column, Integer, String

from app.core.db.sqlalchemy_base_class import Base


class VUserRole(Base):
    __tablename__ = "vaton_user_role"  # type: ignore
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)

    def __repr__(self):
        return f"User Role(id={self.id},role={self.role})"

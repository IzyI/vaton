from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # for ignore sqlalchemy Unexpected keyword argument
    def __init__(self, *args, **kwargs) -> None:
        ...

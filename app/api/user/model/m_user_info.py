from app.api.user.dbmodel.vaton_user_info import VUserInfo
from app.api.user.schemas import BaseUserInfo
from app.core.db.sqlalchemy_crud import CrudBase

ModelUserInfo = CrudBase[VUserInfo, BaseUserInfo, BaseUserInfo]

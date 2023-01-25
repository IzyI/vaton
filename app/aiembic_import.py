"""
You can't delete.
This file is needed to register tables in the commader.py file and clicommand
"""

from app.api.user.dbmodel.vaton_user import VUser  # noqa
from app.api.user.dbmodel.vaton_user_device import VUserDevice  # noqa
from app.api.user.dbmodel.vaton_user_info import VUserInfo  # noqa
from app.api.user.dbmodel.vaton_user_role import VUserRole  # noqa
from app.core.db.sqlalchemy_base_class import Base  # noqa

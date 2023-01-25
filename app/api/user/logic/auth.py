from typing import Optional, Tuple

import cryptocode
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.user.dbmodel.vaton_user import VUser
from app.api.user.dbmodel.vaton_user_device import VUserDevice
from app.api.user.model.m_user import ModelUser
from app.config.settings import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                                 REFRESH_TOKEN_EXPIRE_MINUTES, SECRET,
                                 SECRET_ID)
from app.core.utils.secur import check_time_jwt, decode_jwt, encode_jwt


async def set_token(db: AsyncSession, user: VUser, token: Optional[str] = None):
    if not await ModelUser(VUser).update(db, db_obj=user, obj_in={"token": token}):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")


async def get_user_device(
    db: AsyncSession, token_refresh: str
) -> Tuple[VUserDevice, VUser]:
    try:
        payload = decode_jwt(token_refresh, SECRET, ALGORITHM)
    except Exception:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized, data"
        )
    if not check_time_jwt(payload.get("exp")) or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized, time"
        )

    try:
        user_base = cryptocode.decrypt(payload.get("id"), SECRET_ID).split("/")
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Very bad")
    user = await ModelUser(VUser).get_user_by_email_with_device(db, user_base[0])
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized, user"
        )
    user_device = user.devices
    for i in user_device:
        if i.token == token_refresh:
            return i, user
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized, token"
    )


async def get_token(user: VUser) -> Tuple[str, str]:
    id = cryptocode.encrypt(
        f"{user.email}/{user.id}/{user.user_role[0].role}", SECRET_ID
    )
    token_access = encode_jwt(
        {"id": id, "type": "access"},
        SECRET,
        ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    token_refresh = encode_jwt(
        {"id": id, "type": "refresh"},
        SECRET,
        ALGORITHM,
        REFRESH_TOKEN_EXPIRE_MINUTES,
    )
    return token_access, token_refresh

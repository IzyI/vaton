import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.user.dbmodel.vaton_user import VUser
from app.api.user.dbmodel.vaton_user_device import VUserDevice
from app.api.user.dbmodel.vaton_user_info import VUserInfo
from app.api.user.logic.auth import get_token, get_user_device
from app.api.user.model.m_user import ModelUser
from app.api.user.model.m_user_device import ModelUserDevice
from app.api.user.model.m_user_info import ModelUserInfo
from app.config.settings import (ALLOWED_REGISTRATION_USER, COUNT_DEVICES,
                                 DOMAIN_BLACK_LIST, SALT, USER_ROLE)
from app.core.db.databases import get_db
from app.core.utils.secur import (clean_email, get_password_hash,
                                  is_password_regex, is_password_weak,
                                  is_valid_email, verify_password)
from app.exception_app.base import (APIAccountIsBannedError,
                                    APIMethodBlockError, APIWrongBaseError,
                                    APIWrongCredentialsError)

from . import schemas

login_user = APIRouter(prefix="/login")


@login_user.post(
    "/",
    response_model=schemas.ResponseLoginUser,
    tags=["Login"],
)
async def authentication(
    login: schemas.RequestLogin, request: Request, db: AsyncSession = Depends(get_db)
):
    """
    Login for existing user.
    """
    user = await ModelUser(VUser).get_user_by_email_with_device(db, login.user.email)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")
    if not verify_password(login.user.password, user.password, SALT):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")

    devices = user.devices
    if not len(devices) < COUNT_DEVICES:
        await ModelUserDevice(VUserDevice).remove(db, id=devices[0].id)

    token_access, token_refresh = await get_token(user)

    ip = None
    if request.client:
        ip = request.client.host

    await ModelUserDevice(VUserDevice).create(
        db,
        obj_in=schemas.BaseUserDevice(
            type=login.device.type,
            version=login.device.version,
            state=login.device.state,
            id_user=user.id,
            token=token_refresh,
            ip=ip,
        ),
    )
    return schemas.ResponseLoginUser(
        token_access=token_access,
        token_refresh=token_refresh,
        email=user.email,
        bio=user.user_info.bio,
    )


@login_user.post(
    "/register",
    response_model=schemas.ResponseInfoUser,
    status_code=201,
    tags=["User and Authentication"],
)
async def register_user(
    new_user: schemas.RequestRegistrUser, db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    """
    if not ALLOWED_REGISTRATION_USER:
        raise APIMethodBlockError()
    if not is_valid_email(new_user.email):
        raise APIWrongCredentialsError(msg="Bad email")
    _email = clean_email(new_user.email)
    name, domain = _email.split("@")
    if domain in DOMAIN_BLACK_LIST:
        raise APIAccountIsBannedError(msg=f"Domain {domain} blacklisted")

    db_user_email = await ModelUser(VUser).get_user_by_email(db, _email)
    if db_user_email:
        raise APIWrongBaseError(msg="Email already registered")
    pass_str, pass_msg = is_password_regex(new_user.password)
    if not pass_str:
        raise APIWrongBaseError(msg=pass_msg)
    pass_str = is_password_weak(new_user.password, _email, name)
    if pass_str:
        raise APIWrongBaseError(
            msg="\n".join(
                [pass_str["warning"], " ".join(pass_str["suggestions"])]
            ).strip()
        )

    user = await ModelUser(VUser).create(
        db,
        schemas.BaseUser(
            password=get_password_hash(new_user.password, SALT), email=_email
        ),
    )

    if new_user.info_user:
        username = new_user.info_user.name
    else:
        username = _email.split("@")[0]
    user_info = await ModelUserInfo(VUserInfo).create(
        db,
        schemas.BaseUserInfo(username=username, bio=str(uuid.uuid4()), id_user=user.id),
    )
    base_role = "user"
    await ModelUser(VUser).pin_user_to_role(db, user.id, USER_ROLE[base_role])
    return schemas.ResponseInfoUser(
        id=user.id,
        bio=user_info.bio,
        username=user_info.username,
        email=user.email,
        role=[base_role],
    )


@login_user.post(
    "/token",
    response_model=schemas.ResponseTokenUser,
    tags=["Login"],
)
async def authentication_token_refresh(
    token: schemas.ResponseTokenUser, db: AsyncSession = Depends(get_db)
):
    """
    Login for existing user.
    """
    user_device, user = await get_user_device(db, token.token_refresh)
    token_access, token_refresh = await get_token(user)
    await ModelUserDevice(VUserDevice).update(
        db, db_obj=user_device, obj_in=schemas.BaseUpdateUserDevice(token=token_refresh)
    )
    return schemas.ResponseTokenUser(
        token_access=token_access,
        token_refresh=token_refresh,
    )

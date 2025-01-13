from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.dbmodel.vaton_user import VUser
from app.api.user.model.m_user import ModelUser
from app.api.user.models_mongo import Note
from app.config.settings import ALLOWED_REGISTRATION_USER
from app.core.db.databases import get_db, get_mongo_db
from app.exception_app.base import APIMethodBlockError, APIWrongBaseError

from . import schemas

user = APIRouter()


@user.get(
    "/", response_model=schemas.ResponseInfoUser, tags=["User and Authentication"]
)
async def current_user(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Gets the currently logged-in user.
    """
    user = await ModelUser(VUser).get(db, id=request.state.current_user.id)
    if not user:
        raise APIWrongBaseError(msg="Not found user")
    return schemas.ResponseInfoUser(
        id=user.id,
        bio=user.user_info.bio,
        username=user.user_info.username,
        email=user.email,
        role=[i.role for i in user.user_role],
    )


@user.delete("/", tags=["User and Authentication"])
async def delete_user(request: Request, db: AsyncSession = Depends(get_db)):
    if not ALLOWED_REGISTRATION_USER:
        raise APIMethodBlockError()
    user = await ModelUser(VUser).get(db, id=request.state.current_user.id)
    if not user:
        raise APIWrongBaseError(msg="Not found user")
    await ModelUser(VUser).remove(db, id=user.id)
    return {"result": True}


@user.get(
    "/note", response_model=list[schemas.BaseUserNote], tags=["User and Authentication"]
)
async def user_note(
    db: AsyncSession = Depends(get_mongo_db),
):
    note = await Note(db).get_by_email("example.com")
    return note

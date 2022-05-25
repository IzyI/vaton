from typing import Optional

from pydantic import BaseModel, Field


# ----------------- BASE  ----------------------


class Device(BaseModel):
    type: str = Field(..., max_length=100)
    version: str = Field(..., max_length=7)
    state: str = Field(..., max_length=250)


class BaseUserDevice(Device):
    id_user: int
    token: str
    ip: str


class BaseUpdateUserDevice(BaseModel):
    type: Optional[str] = Field(..., max_length=100)
    version: Optional[str] = Field(..., max_length=7)
    state: Optional[str] = Field(..., max_length=250)
    id_user: Optional[str]
    token: Optional[str]
    ip: Optional[str]


class BaseUser(BaseModel):
    email: str = Field(..., max_length=250)
    password: str = Field(..., max_length=250)


class BaseUserNote(BaseModel):
    email: str = Field(..., max_length=250)
    text: Optional[str]


class BaseUserInfo(BaseModel):
    username: str = Field(..., max_length=250)
    bio: str
    id_user: int


class BaseUserRole(BaseModel):
    role: str
    id: int


class InfoUser(BaseModel):
    name: str = Field(..., max_length=250)


class RequestRegistrUser(BaseUser):
    info_user: Optional[InfoUser]


class RequestLogin(BaseModel):
    device: Device
    user: BaseUser


class ResponseLoginUser(BaseModel):
    token_access: str
    token_refresh: str
    email: str
    bio: Optional[str] = Field(..., max_length=36)


class ResponseInfoUser(BaseModel):
    id: int
    username: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    role: Optional[list[str]] = None


class ResponseTokenUser(BaseModel):
    token_access: Optional[str]
    token_refresh: str

from typing import Optional

from pydantic import BaseModel, Field


class VersionShema(BaseModel):
    name: str
    version: str


class PingShema(BaseModel):
    result: str = "pong"


class ErrorBaseSchema(BaseModel):
    msg: str = Field(..., example="message error")
    type: str = Field(..., example="type error")
    error_code: int = Field(..., example="code error")
    data: Optional[dict] = Field(..., example="payload, additional parameters")


class ErrorValidationSchema(BaseModel):
    msg: str = "Validation Error"
    error_code: int = 1422
    type: str = "RequestValidationError"
    data: dict = Field(
        ..., example={"details": [{"loc": [], "msg": "string", "type": "string"}]}
    )

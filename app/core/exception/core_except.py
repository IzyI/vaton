from typing import Any, Dict, Optional

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

"""
error_code 1000...1399 / 1500...2000
"""


class BaseLogicException(HTTPException):
    msg: str = "Bad Logic Request"
    error_header: str = "Bad Request"
    error_code: int = 1400
    data: Optional[dict] = None
    headers = None
    status_code = 400
    type = "BaseLogicException"

    def __init__(
        self,
        msg: Optional[str] = None,
        error_header: Optional[str] = None,
        error_code: Optional[int] = None,
        data: Optional[dict] = None,
        headers: Optional[Dict[str, Any]] = None,
        status_code: Optional[int] = None,
        type: Optional[str] = None,  # noqa
    ) -> None:
        self.msg = msg or self.msg
        self.error_header = error_header or self.error_header
        self.status_code = status_code or self.status_code
        self.headers = headers or self.headers
        self.type = type or self.type
        self.data = data or self.data
        self.error_code = error_code or self.error_code


def http_base_logic_exception_handler(_, exc: BaseLogicException):
    result_json = {
        "msg": exc.msg,
        "type": exc.type,
        "error_code": exc.error_code,
        "error_header": exc.error_header,
    }
    if exc.data:
        result_json["data"] = exc.data
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(result_json),
        headers=exc.headers,
    )


async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "msg": "Validation Error",
                "type": "RequestValidationError",
                "data": {"details": exc.errors()},
                "error_code": 1422,
            }
        ),
    )

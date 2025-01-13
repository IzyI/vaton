from app.config.settings import PROJECT_ADMIN_EMAIL
from app.core.exception.core_except import BaseLogicException


class APIWrongCredentialsError(BaseLogicException):
    msg = "Please check if you've typed your email and password correctly."
    error_header = "Wrong email or password"
    error_code = 1422
    status_code = 422
    type = "APIWrongCredentialsError"


class APIWrongBaseError(BaseLogicException):
    msg = "Please check if you've typed your email and password correctly."
    error_header = "Base Error"
    error_code = 1
    type = "APIWrongBaseError"


class APINotFound(BaseLogicException):
    msg = "I didn't find anything."
    error_header = "Not fount"
    error_code = 1
    type = "APIWrongBaseError"


class APIMethodBlockError(BaseLogicException):
    msg = "The method is blocked by the admin."
    error_header = "Method Block"
    error_code = 2
    type = "APIMethodBlockError"


class APIAccountIsBannedError(BaseLogicException):
    error_code = 1422
    status_code = 422
    error_header = "Has been banned"
    error_description = (
        f"You are banned , please contact the admin {PROJECT_ADMIN_EMAIL}"
    )
    type = "APIAccountIsBannedError"

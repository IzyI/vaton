from typing import Optional

import cryptocode
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config.settings import ALGORITHM, SECRET, SECRET_ID
from app.core.utils.secur import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )
            try:
                payload = decode_jwt(credentials.credentials, SECRET, ALGORITHM)
            except Exception:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized  token"
                )
            if payload.get("type") == "refresh":
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication type.",
                )
            else:
                try:
                    user = cryptocode.decrypt(payload["id"], SECRET_ID)
                    u = user.split("/")

                    class User:
                        email: str = u[0]
                        id: int = int(u[1])
                        role: str = u[2]

                    request.state.current_user = User
                except Exception:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Invalid authorization payload.",
                    )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authorization code."
            )

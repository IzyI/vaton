import time

from fastapi import APIRouter, Depends, FastAPI, Header, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.user.authorize import JWTBearer
from app.api.user.router import login_user, router_user
from app.config.settings import (ALLOWED_HOSTS, API_V1_STR, DB_MAX_OVERFLOW,
                                 DB_POOL_SIZE, DB_TIMEOUT, PROJECT_NAME,
                                 SQLALCHEMY_DATABASE_URI, VERSION)
from app.core.db.databases import create_engine_async_app
from app.core.exception.core_except import (BaseLogicException,
                                            http_base_logic_exception_handler,
                                            validation_exception_handler)
from app.core.schema.core_schema import (ErrorBaseSchema, PingShema,
                                         VersionShema)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def create_app() -> FastAPI:
    node = FastAPI(
        responses={
            400: {"model": ErrorBaseSchema},
            # 422: {"model": ErrorValidationSchema},
        },
    )
    node.add_exception_handler(RequestValidationError, validation_exception_handler)
    node.add_exception_handler(BaseLogicException, http_base_logic_exception_handler)
    engine, sessionmaker = create_engine_async_app(
        SQLALCHEMY_DATABASE_URI,
        pool_size=DB_POOL_SIZE,
        max_overflow=DB_MAX_OVERFLOW,
        pool_timeout=DB_TIMEOUT,
    )
    node.state.engine = engine
    node.state.sessionmaker = sessionmaker

    # ----

    node.include_router(login_user, prefix=f"/api/{API_V1_STR}")
    admin_route = APIRouter(prefix="/user")
    admin_route.include_router(router_user)

    # ----
    node.include_router(
        admin_route, prefix=f"/api/{API_V1_STR}", dependencies=[Depends(JWTBearer())]
    )

    @node.get("/ping", tags=["check"], response_model=PingShema)
    def ping():
        return {"result": "pong"}

    @node.get("/version", tags=["check"], response_model=VersionShema)
    def version():
        return {"version": VERSION, "name": PROJECT_NAME}

    node.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @node.middleware("http")
    async def add_time_headers(request: Request, call_next):
        """
        Adds time headers to check the time spent on the particular request
        """

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return node


app = create_app()

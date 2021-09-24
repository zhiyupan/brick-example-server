import asyncio
from typing import Any, AsyncGenerator, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from brick_server.minimal.app import app as fastapi_app
from brick_server.minimal.auth.authorization import create_jwt_token
from brick_server.minimal.models import User
from brick_server.minimal.tests.utils import register_admin


@pytest.yield_fixture(scope="session")
def event_loop(request: Any) -> Generator[asyncio.AbstractEventLoop, Any, Any]:
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    # loop.close()


@pytest.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, Any]:
    async with LifespanManager(fastapi_app):
        yield fastapi_app


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c


@pytest.fixture(scope="session")
def admin_user(app: FastAPI) -> User:
    return register_admin(user_id="admin")


@pytest.fixture(scope="session")
def admin_jwt(admin_user: User) -> str:
    token = create_jwt_token(
        user_id=admin_user.user_id,
        app_name="brickserver_frontend",
    )
    print(token)
    return token


@pytest.fixture(scope="session")
def admin_headers(admin_jwt: str):
    headers = {"Authorization": "Bearer " + admin_jwt}
    return headers

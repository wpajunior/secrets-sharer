from typing import Callable

from fastapi import FastAPI

from ..repositories.events import close_connection_pool, create_connection_pool


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app():
        app.state.pool = await create_connection_pool()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app():
        await close_connection_pool(app.state.pool)

    return stop_app

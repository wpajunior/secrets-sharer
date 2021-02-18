from typing import Any, Callable, Coroutine

from fastapi import FastAPI

from app.repositories.events import (close_connection_pool,
                                     create_connection_pool)


def create_start_app_handler(
    app: FastAPI
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        app.state.pool = await create_connection_pool()

    return start_app


def create_stop_app_handler(
    app: FastAPI
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def stop_app() -> None:
        await close_connection_pool(app.state.pool)

    return stop_app

from aioredis.commands import Redis
from fastapi import Depends
from starlette.requests import Request

from app.repositories.secrets import RedisSecretsRepository, SecretsRepository
from app.services.id import id_generator


def get_repository_pool(request: Request) -> Redis:
    return request.app.state.pool


async def get_secrets_repository(
        pool: Redis = Depends(get_repository_pool)) -> SecretsRepository:
    return RedisSecretsRepository(pool, id_generator())

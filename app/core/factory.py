from fastapi import Depends
from starlette.requests import Request

from ..repositories.secrets import RedisSecretsRepository, SecretsRepository
from ..services.id import id_generator


def get_repository_pool(request: Request):
    return request.app.state.pool


async def get_secrets_repository(
        pool=Depends(get_repository_pool)) -> SecretsRepository:
    return RedisSecretsRepository(pool, id_generator())

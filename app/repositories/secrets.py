from abc import ABC, abstractmethod
from typing import Generator

import aioredis

from app.models.domain.secrets import Secret

from .errors import SecretDoesNotExist


class SecretsRepository(ABC):
    @abstractmethod
    async def get(self, id: str) -> Secret:
        raise NotImplementedError

    @abstractmethod
    async def create(self, secret: Secret) -> Secret:
        raise NotImplementedError

    @abstractmethod
    async def update(self, secret: Secret) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError


class RedisSecretsRepository(SecretsRepository):
    def __init__(
        self, redis: aioredis.RedisConnection, id_generator: Generator[str, None, None]
    ) -> None:
        self.redis = redis
        self.id_generator = id_generator

    async def get(self, id: str) -> Secret:
        secret_dict = await self.redis.hgetall(id)

        if not secret_dict:
            raise SecretDoesNotExist(f"Secret with id '{id}' was not found")

        ttl = await self.redis.ttl(id)

        return Secret(id=id, ttl=ttl, **secret_dict)

    async def create(self, secret: Secret) -> Secret:
        secret_out: Secret = Secret(
            id=next(self.id_generator), **secret.dict(exclude_unset=True)
        )

        await self.redis.hmset_dict(
            secret_out.id, **secret.dict(exclude_unset=True, exclude={"ttl"})
        )

        await self.redis.expire(secret_out.id, secret_out.ttl)

        return secret_out

    async def update(self, secret: Secret) -> None:
        await self.redis.hmset_dict(
            secret.id, **secret.dict(exclude_unset=True, exclude={"id", "ttl"})
        )

    async def delete(self, id: str) -> None:
        await self.redis.delete(id)

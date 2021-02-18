from abc import ABC, abstractmethod
from typing import Generator

import aioredis

from ..schemas.secrets import (SecretCreateIn, SecretDb, SecretOut,
                               SecretUpdateIn)
from .errors import SecretDoesNotExist


class SecretsRepository(ABC):
    @abstractmethod
    async def get(self, id: str) -> SecretOut:
        raise NotImplementedError

    @abstractmethod
    async def create(self, secret: SecretCreateIn) -> SecretOut:
        raise NotImplementedError

    @abstractmethod
    async def update(self, secret: SecretUpdateIn) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError


class RedisSecretsRepository(SecretsRepository):
    def __init__(
                 self, redis: aioredis.RedisConnection,
                 id_generator: Generator[str, None, None]) -> None:
        self.redis = redis
        self.id_generator = id_generator

    async def get(self, id: str) -> SecretOut:
        secret_dict = await self.redis.hgetall(id)

        if not secret_dict:
            raise SecretDoesNotExist(f"Secret with id '{id}' was not found")

        ttl = await self.redis.ttl(id)

        return SecretOut(id=id, ttl=ttl, **secret_dict)

    async def create(self, secret: SecretCreateIn) -> SecretOut:
        secret_out: SecretOut = SecretOut(
            id=next(self.id_generator),
            **secret.dict(exclude_unset=True)
        )
        secret_db: SecretDb = SecretDb(**secret.dict(exclude_unset=True))

        await self.redis.hmset_dict(
            secret_out.id,
            **secret_db.dict(exclude_unset=True)
        )

        await self.redis.expire(secret_out.id, secret_out.ttl)

        return secret_out

    async def update(self, secret: SecretUpdateIn) -> None:
        secret_db: SecretDb = SecretDb(**secret.dict(exclude_unset=True))

        await self.redis.hmset_dict(
            secret.id,
            **secret_db.dict(exclude_unset=True)
        )

    async def delete(self, id: str) -> None:
        await self.redis.delete(id)

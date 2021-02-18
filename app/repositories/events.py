from aioredis import ConnectionsPool, create_redis_pool
from aioredis.abc import AbcPool

from app.core.config import DATABASE_URL


async def create_connection_pool() -> ConnectionsPool:
    return await create_redis_pool(DATABASE_URL)


async def close_connection_pool(pool: AbcPool) -> None:
    pool.close()
    await pool.wait_closed()

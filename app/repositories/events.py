from aioredis import create_redis_pool
from aioredis.abc import AbcPool

from ..core.config import DATABASE_URL


async def create_connection_pool():
    return await create_redis_pool(DATABASE_URL)


async def close_connection_pool(pool: AbcPool):
    pool.close()
    await pool.wait_closed()

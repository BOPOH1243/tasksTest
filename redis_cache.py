import redis.asyncio as redis
import os
from datetime import timedelta

REDIS_URL = os.getenv('REDIS_URL', "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
async def get_redis():
    '''затычка для асинхронного редиса'''
    try:
        yield redis_client
    finally:
        await redis_client.close()

async def store_refresh_token(username: str, refresh_token: str, expires_in: timedelta):
    await redis_client.setex(f"refresh_token:{username}", expires_in, refresh_token)

async def get_refresh_token(username: str):
    return await redis_client.get(f"refresh_token:{username}")

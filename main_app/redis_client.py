import redis
import logging

from fastapi import Request
from fastapi.responses import HTMLResponse

from functools import wraps


def get_redis_client():
    return redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


async def redis_dependency():
    client = get_redis_client()
    try:
        yield client
    finally:
        client.close()

def cache_page(expire_time=3600): 
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = next((v for v in kwargs.values() if isinstance(v, Request)), None)
            if not request:
                return await func(*args, **kwargs)

            redis_client = get_redis_client()
            cache_key = f"page_cache:{request.url.path}"

            cached_response = redis_client.get(cache_key)
            if cached_response:
                print("Cache hit")
                return HTMLResponse(content=cached_response)

            response = await func(*args, **kwargs)

            if hasattr(response, 'body'):
                redis_client.setex(
                    cache_key,
                    expire_time,
                    response.body.decode()
                )

            return response
        return wrapper
    return decorator
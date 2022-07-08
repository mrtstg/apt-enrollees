import aioredis
from configs.reader import get_config_variable
import orjson as json

def _get_redis_connection() -> aioredis.Redis:
    return aioredis.Redis(
        host=get_config_variable('redis.host'),
        port=get_config_variable('redis.port'),
        decode_responses=True
    )

def redis_cache(timeout: int = 30):
    
    def _redis_cache(f):

        async def __redis_cache(*args, **kwargs):
            redis = _get_redis_connection()

            key_parts = [f.__name__] + list(map(str, args)) + [f'{key}-{value}' for key, value in kwargs.items()]
            key = '-'.join(key_parts)
            result = await redis.get(key)

            if result is None:
                value = await f(*args, **kwargs)
                value_json = json.dumps(value)
                await redis.set(key, value_json, ex=timeout)
            else:
                value = json.loads(result)

            await redis.close()
            return value
        
        return __redis_cache
    
    return _redis_cache
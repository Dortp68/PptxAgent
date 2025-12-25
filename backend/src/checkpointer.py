from langgraph.checkpoint.redis.aio import AsyncRedisSaver
import redis.asyncio as redis
from src.utils import logger
from src.utils import config

async def init_checkpointer():
    """Async Redis Checkpointer Initialization"""
    redis_client = redis.Redis(host=config.redis.host,
                               port=config.redis.port,
                               db=config.redis.db,
                               decode_responses=False)
    try:
        async with AsyncRedisSaver.from_conn_string(redis_client=redis_client) as checkpointer:
            await checkpointer.asetup()
            logger.info("✅ AsyncRedisSaver initialized")
            return checkpointer
    except Exception as e:
        """TODO: fallback to in-memory checkpointer"""
        logger.error(f"❌ Init error Redis: {e}")
        return None
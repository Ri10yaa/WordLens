"""Redis-backed caching helpers."""

import json
from typing import Optional

import redis

from app.core.config import settings


redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=False,
)


def cache_word(word: str, normalized_data: dict, ttl: int = settings.cache_ttl):
    redis_client.setex(
        f"word:{word.lower()}",
        ttl,
        json.dumps(normalized_data),
    )


def get_cached_word(word: str) -> Optional[dict]:
    data = redis_client.get(f"word:{word.lower()}")
    if not data:
        return None
    return json.loads(data)

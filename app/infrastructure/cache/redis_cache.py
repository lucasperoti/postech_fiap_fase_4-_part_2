import json
from typing import Any

import redis

from app.core.config import settings


class RedisCache:
    def __init__(self):
        self._client = redis.from_url(settings.redis_url, decode_responses=True)

    def get(self, key: str) -> Any | None:
        value = self._client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        self._client.setex(key, ttl, json.dumps(value, default=str))

    def delete(self, key: str) -> None:
        self._client.delete(key)

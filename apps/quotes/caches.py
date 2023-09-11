from typing import Any

import json

from django.conf import settings

from apps.accounts.models import CustomUser
from apps.utils.redis_pool import RedisPoolManager


def get_cache_key(user: CustomUser, base_key: str = 'values_list'):
    if user.is_authenticated:
        cache_key = f'{base_key}:{user.id}'
    else:
        cache_key = base_key
    return cache_key


def get_sorted_cached_data(cached_data, order_by: str):
    if order_by[0] == '-':
        order_by = order_by.replace('-', '')
        sorted_cached_data = sorted(cached_data, key=lambda o: -o[order_by])
    else:
        sorted_cached_data = sorted(cached_data, key=lambda o: o[order_by])
    return sorted_cached_data


class QuotesRedisCache:
    BASE_KEY = 'quotes_cache'

    def __init__(self, host: str = None, port: int = None):
        if host is None:
            host = settings.REDIS_HOST
        if port is None:
            port = settings.REDIS_PORT
        pool_manager = RedisPoolManager(host, port)
        self.connection = pool_manager.get_connection()

    def _build_key(self, key: str):
        return f'{self.BASE_KEY}:{key}'

    def get_data_from_cache(self, key: str):
        key = self._build_key(key)
        cached_data = self.connection.get(key)
        if cached_data is not None:
            cached_data = json.loads(cached_data)
        else:
            cached_data = None
        return cached_data

    def set_data_to_cache(self, key: str, data: Any,):
        key = self._build_key(key)
        self.connection.set(key, json.dumps(data))

    def delete_data_from_cache(self):
        keys = self.connection.keys(f'{self.BASE_KEY}*')
        self.connection.delete(*keys)

import redis
from urllib.parse import urlparse


class RedisPoolManager:
    def __init__(self, url='redis://localhost:6379', max_connections=1):
        parsed_url = urlparse(url)
        host, port = parsed_url.hostname, parsed_url.port

        self.pool = redis.ConnectionPool(host=host, port=port, max_connections=max_connections)
        self.connection = redis.StrictRedis(connection_pool=self.pool)

    def get_connection(self):
        return self.connection

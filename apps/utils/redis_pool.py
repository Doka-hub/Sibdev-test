import redis


class RedisPoolManager:
    def __init__(self, host: str, port: int, max_connections=10):
        self.pool = redis.ConnectionPool(host=host, port=port, max_connections=max_connections)
        self.connection = redis.StrictRedis(connection_pool=self.pool)

    def get_connection(self):
        return self.connection

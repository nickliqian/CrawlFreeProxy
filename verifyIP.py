import redis
from tools.common import test_proxy
import requests

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
CONN_REDIS = redis.Redis(connection_pool=POOL)

proxy = CONN_REDIS.lpop("freeProxy:BeforeVerifyhttp")


proxy = str(proxy, encoding="utf-8")

test_proxy()

CONN_REDIS.rpush("freeProxy:BeforeVerifyhttp", proxy)

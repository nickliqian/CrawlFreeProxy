from gevent import monkey;monkey.patch_socket();monkey.patch_ssl();monkey.patch_time()
import gevent
import redis
from tools.settings import *

if __name__ == '__main__':

    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
    CONN_REDIS = redis.Redis(connection_pool=POOL)

    # 动态获取所有方法
    jobs = []
    for attr in dir():
        if attr.startswith("proxy__"):
            if attr not in ["proxy__test"]:
                # 所有proxy__开头的方法都加入jobs列表
                jobs.append(gevent.spawn(locals()[attr], CONN_REDIS))

    # 使用协程执行jobs列表中的函数，并返回结果
    results = gevent.joinall(jobs)

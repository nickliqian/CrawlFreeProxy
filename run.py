from multiprocessing import Process
import threading
import web_app
from module import verifyIP
import redis


def crawlIP():

    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
    CONN_REDIS = redis.Redis(connection_pool=POOL)

    # 动态获取所有方法
    from tools.settings import *
    jobs = []
    print(dir())
    for attr in dir():
        if attr.startswith("proxy__"):
            if attr not in ["proxy__test"]:
                # 所有proxy__开头的方法都加入jobs列表
                jobs.append(threading.Thread(target=locals()[attr], args=(CONN_REDIS,)))

    # 开启多线程
    for t in jobs:
        t.start()

    for t in jobs:
        t.join()


def run_web():
    web_app.run(host="0.0.0.0", port=7865)


def run():
    print('代理池开始运行')

    crawl_process = Process(target=crawlIP)
    crawl_process.start()

    verify_process = Process(target=verifyIP.main)
    verify_process.start()

    web_process = Process(target=run_web)
    web_process.start()

if __name__ == '__main__':
    run()
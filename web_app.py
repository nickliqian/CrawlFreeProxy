from flask import Flask, g, render_template
from multiprocessing import Process
from module import crawlIP, verifyIP, verifyHTTPSip
import redis
import threading
from tools.settings import *


__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'conn_redis'):
        redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        g.conn_redis = redis.Redis(connection_pool=redis_pool)
    return g.conn_redis


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_http')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return str(conn.srandmember("freeProxy:AfterVerifyOKhttp", 1))


@app.route('/random_https')
def get_proxy_s():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return str(conn.srandmember("freeProxy:AfterVerifyOKhttps", 1))


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    """
    1) "freeProxy:BeforeVerifyhttp"
2) "freeProxy:BeforeVerifyhttps"
3) "freeProxy_Bad:AfterVerifyFailhttp"

    """
    http_before = conn.scard("freeProxy:BeforeVerifyhttp")
    https_before = conn.scard("freeProxy:BeforeVerifyhttps")
    http_after_bad = conn.scard("freeProxy_Bad:AfterVerifyFailhttp")
    https_after_bad = conn.scard("freeProxy_Bad:AfterVerifyFailhttps")
    http_after_ok = conn.scard("freeProxy:AfterVerifyOKhttp")
    https_after_ok = conn.scard("freeProxy:AfterVerifyOKhttps")

    return render_template('count.html',
                           http_before=http_before,
                           https_before=https_before,
                           http_after_bad=http_after_bad,
                           https_after_bad=https_after_bad,
                           http_after_ok=http_after_ok,
                           https_after_ok=https_after_ok)


if __name__ == '__main__':
    print('代理池开始运行')

    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
    CONN_REDIS = redis.Redis(connection_pool=POOL)

    # 动态获取所有方法
    jobs = []
    print(dir())
    for attr in dir():
        if attr.startswith("proxy__"):
            if attr not in ["proxy__test", "proxy__nianshao"]:
                # 所有proxy__开头的方法都加入jobs列表
                jobs.append(threading.Thread(target=locals()[attr], args=(CONN_REDIS,)))

    # 开启多线程
    for t in jobs:
        t.start()

    # crawl_process = Process(target=crawlIP.main, args=(func_var,))
    # crawl_process.start()

    verify_process = Process(target=verifyIP.main)
    verify_process.start()

    verify_https_process = Process(target=verifyHTTPSip.main)
    verify_https_process.start()

    app.run(host="0.0.0.0", port=7865)

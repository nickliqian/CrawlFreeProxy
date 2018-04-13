import redis
from tools.common import test_http_proxy, test_https_proxy
import threading
import time


# 测试新入的IP
def verify_fresh_proxy(name, before, after_ok, after_bad, call_func):
    # 连接redis数据库
    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
    CONN_REDIS = redis.Redis(connection_pool=POOL)
    print("INFO: Start proxy verify {}".format(name))
    while True:
        # 取出一个ip进行测试
        proxy = CONN_REDIS.spop(before)
        # 判断redis中ip数量是否为空
        if not proxy:
            print("INFO: {} 等待ip入队列 {}".format(name, before))
            time.sleep(60)
        else:
            print("INFO: {} Get proxy from Redis {} list".format(name, before))
            proxy = str(proxy, encoding="utf-8")
            flag = call_func(proxy)
            if flag:
                CONN_REDIS.sadd(after_ok, proxy)
                print("INFO: {} Save this Proxy IP in {}".format(name, after_ok))
            else:
                CONN_REDIS.sadd(after_bad, proxy)
                print("INFO: {} Abandon this Proxy IP to {}!".format(name, after_bad))


# 测试之前通过的IP，周期半小时
def verify_ok_proxy(name, before, after_ok, after_bad, call_func):
    print(before)
    # 连接redis数据库
    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
    CONN_REDIS = redis.Redis(connection_pool=POOL)
    while True:
        print("INFO: Start proxy verify {}", format(name))
        # 取出一个ip进行测试
        all_ip = CONN_REDIS.smembers(after_ok)
        for ip_b in all_ip:
            proxy = str(ip_b, encoding="utf-8")
            flag = call_func(proxy)
            if not flag:
                CONN_REDIS.srem(after_ok, proxy)
                CONN_REDIS.sadd(after_bad, proxy)
                print("INFO: {} Proxy {} removed from {}".format(name, proxy, after_ok))
            else:
                print("INFO: {} Proxy {} is OK".format(name, proxy))
        print("{} 等待下一轮验证".format(name))
        time.sleep(1800)


def fresh_proxy_thread_task():

    # HTTP代理仓库名称
    http_before = "freeProxy:BeforeVerifyhttp"
    http_after_ok = "freeProxy:AfterVerifyOKhttp"
    http_after_bad = "freeProxy_Bad:AfterVerifyFailhttp"
    # HTTPS代理仓库名称
    https_before = "freeProxy:BeforeVerifyhttps"
    https_after_ok = "freeProxy:AfterVerifyOKhttps"
    https_after_bad = "freeProxy_Bad:AfterVerifyFailhttps"

    # 线程配置
    jobs_http = []
    jobs_https = []
    num = 5

    # HTTP线程
    # 新proxy验证线程
    for i in range(1, num+1):
        name = "Thread-http" + str(i)
        jobs_http.append(threading.Thread(target=verify_fresh_proxy,
                                          args=(name, http_before, http_after_ok, http_after_bad, test_http_proxy,)))
    # pass proxy反复验证线程，周期半小时
    name1 = "Thread-ok_http_verify"
    job_ok_http = threading.Thread(target=verify_fresh_proxy,
                                   args=(name1, https_before, https_after_ok, https_after_bad, test_http_proxy,))

    # HTTPS线程
    # 新proxy验证线程
    for i in range(1, num+1):
        name = "Thread-https" + str(i)
        jobs_https.append(threading.Thread(target=verify_fresh_proxy,
                                           args=(name, https_before, https_after_ok, https_after_bad, test_https_proxy,)))
    # pass proxy反复验证线程，周期半小时
    name2 = "Thread-ok_https_verify"
    job_ok_https = threading.Thread(target=verify_fresh_proxy,
                                    args=(name2, https_before, https_after_ok, https_after_bad, test_https_proxy,))

    # 开启多线程
    for t in jobs_http:
        t.start()
    job_ok_http.start()

    for t in jobs_https:
        t.start()
    job_ok_https.start()


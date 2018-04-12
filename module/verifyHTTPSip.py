import redis
from tools.common import test_http_proxy
import threading
import time


def http_task():
    # 连接redis数据库
    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
    CONN_REDIS = redis.Redis(connection_pool=POOL)
    # 取出一个ip进行测试
    proxy = CONN_REDIS.spop("freeProxy:BeforeVerifyhttps")
    # 判断redis中ip数量是否为空
    if not proxy:
        print("等待ip入队列")
        time.sleep(30)
        # return 0
    else:
        print("INFO: Get proxy from Redis freeProxy:BeforeVerifyhttps list")
        proxy = str(proxy, encoding="utf-8")
        flag = test_http_proxy(proxy)
        if flag == True:
            CONN_REDIS.sadd("freeProxy:AfterVerifyOKhttps", proxy)
            print("INFO: Save this Proxy IP in freeProxy:AfterVerifyOKhttps")
        else:
            CONN_REDIS.sadd("freeProxy_Bad:AfterVerifyFailhttps", proxy)
            print("INFO: Abandon this Proxy IP!")
        return 1


def loop_test(name):
    print("*Start thread task %s" % name)
    while True:
        result = http_task()
        print("\n")
        if result == 0:
            break


def main():
    jobs = []
    num = 8
    for i in range(1, num+1):
        name = "Thread-" + str(i)
        jobs.append(threading.Thread(target=loop_test, args=(name,)))

    # 开启多线程
    for t in jobs:
        t.start()

    for t in jobs:
        t.join()


if __name__ == "__main__":
    main()

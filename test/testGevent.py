# 如果是http请求使用协程，需要导入patch_socket
from gevent import monkey;monkey.patch_socket()
import gevent
import requests
from lxml import etree
import time

"""
    高匿代理IP
    西刺代理
        http://www.xicidaili.com/nn/ + str(offset)
        offset in range(1,6)

"""


class CrawlProxy(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/62.0.3202.62 Safari/537.36", }

    # 使用xpath解析，如果解析为空就返回None，避免抛出异常
    @staticmethod
    def if_empty_list(dom, exp):
        lis = dom.xpath(exp)
        if not lis:
            return None
        else:
            return lis[0]

    def proxy_xici(self):
        s = time.time()
        url = "http://www.baidu.com/nn/"
        def parse_info():
            # print(url)
            response = requests.get(url=url, headers=self.headers, timeout=10)
            # print(url, response)

        jobs = [gevent.spawn(parse_info) for i in range(10)]
        gevent.joinall(jobs)
        e = time.time()
        print("Gevent:", float(e) - float(s))

    def proxy_xici_2(self):
        s = time.time()
        url = "http://www.baidu.com/nn/"
        for offset in range(10):
            # print(url)
            response = requests.get(url=url, headers=self.headers, timeout=10)
            # print(url, response)

        e = time.time()
        print("Normal:", float(e) - float(s))


c = CrawlProxy()
c.proxy_xici()
print("-----------")
c.proxy_xici_2()
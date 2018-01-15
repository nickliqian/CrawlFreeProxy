# 如果是http请求使用协程，需要导入patch_socket
from gevent import monkey;monkey.patch_socket()
import gevent
import requests
from lxml import etree
import time
import json


"""
    高匿代理IP
    西刺代理
        http://www.xicidaili.com/nn/ + str(offset)
        offset in range(1,6)
        
"""


class CrawlProxy(object):

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/62.0.3202.62 Safari/537.36",}

    # 使用xpath解析，如果解析为空就返回None，避免抛出异常
    @staticmethod
    def if_empty_list(dom, exp):
        lis = dom.xpath(exp)
        if not lis:
            return None
        else:
            return lis[0]

    def proxy_xici(self):
        print("*Start -> XiCi Proxy")
        base_url = "http://www.xicidaili.com/nn/"
        start = 1
        end = 3
        def parse_info(offset):
            url = base_url + str(offset)
            response = requests.get(url=url, headers=self.headers, timeout=10)
            print("***run -> XiCi Proxy", url, response)
            html = etree.HTML(response.text)
            rows = html.xpath("//table[@id='ip_list']//tr")
            items = []
            for row in rows:
                item = {}
                item['ip'] = self.if_empty_list(row, "./td[2]/text()")
                item['port'] = self.if_empty_list(row, "./td[3]/text()")
                item['protocol'] = self.if_empty_list(row, "./td[6]/text()")
                items.append(item)
            return items
        jobs = [gevent.spawn(parse_info, offset) for offset in range(start, end)]

        result = gevent.joinall(jobs)
        results = [ge_obj.value for ge_obj in result]
        origin = []
        for value in results:
            origin.extend(value)
        print("*Finish -> XiCi Proxy")
        return origin

    def proxy_xundaili(self):
        print("*Start -> XunDaiLi Proxy")
        # 10分钟更新一次
        url = "http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10"
        response = requests.get(url=url, headers=self.headers, timeout=10)
        print("***run -> XunDaiLi Proxy", url, response)
        dic = json.loads(response.text)
        ip_list = dic["RESULT"]["rows"]
        items = []
        for ip in ip_list:
            item = {}
            if ip["anony"] == "高匿":
                item['ip'] = ip["ip"] + ":" + ip["port"]
                if ip["type"] == "HTTP/HTTPS":
                    item['protocol'] = "http/https"
                items.append(item)
        print("*Finish -> XunDaiLi Proxy")
        return items

    def proxy_wuyou(self):
        print("*Start -> WuYou Proxy")
        url = "http://www.data5u.com/free/gngn/index.shtml"
        response = requests.get(url=url, headers=self.headers, timeout=10)
        print("***run -> WuYou Proxy", url, response)
        html = etree.HTML(response.text)
        rows = html.xpath("//div[@class='wlist']/ul/li/ul")
        items = []
        for row in rows[1:]:
            item = {}
            item['ip'] = self.if_empty_list(row, "./span[1]/li/text()")
            item['port'] = self.if_empty_list(row, "./span[2]/li/text()")
            item['protocol'] = self.if_empty_list(row, "./span[4]/li/a/text()")
            items.append(item)
        print("*Finish -> WuYou Proxy")
        return items

c = CrawlProxy()
jobs = [
    gevent.spawn(c.proxy_wuyou),
    gevent.spawn(c.proxy_xundaili),
    gevent.spawn(c.proxy_xici),
]

results = gevent.joinall(jobs)
for result in results:
    for value in result.value:
        print(value)

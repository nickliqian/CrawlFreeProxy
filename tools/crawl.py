# 如果是http请求使用协程，需要导入patch_socket
from gevent import monkey;monkey.patch_socket();monkey.patch_ssl()
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

    # 西刺代理 12h 5p
    def proxy__xici(self):
        print("*Start -> XiCi Proxy")
        base_url = "http://www.xicidaili.com/nn/"
        start = 1
        end = 2
        def parse_info(offset):
            url = base_url + str(offset)
            print("***begin -> XiCi Proxy", url)
            response = requests.get(url=url, headers=self.headers, timeout=10)
            print("***run -> XiCi Proxy", url, response)
            html = etree.HTML(response.text)
            rows = html.xpath("//table[@id='ip_list']//tr[@class]")
            items = []
            for row in rows:
                item = {}
                ip = self.if_empty_list(row, "./td[2]/text()")
                print(ip)
                port = self.if_empty_list(row, "./td[3]/text()")
                if ip and port:
                    item['ip'] = ip + ":" + port
                    item['protocol'] = self.if_empty_list(row, "./td[6]/text()")
                    items.append(item)
            return items
        jobs = [gevent.spawn(parse_info, offset) for offset in range(start, end+1)]

        result = gevent.joinall(jobs)
        results = [ge_obj.value for ge_obj in result]
        origin = []
        for value in results:
            origin.extend(value)
        print("*Finish -> XiCi Proxy")
        return origin

    # 讯代理 10min 1p
    def proxy__xundaili(self):
        print("*Start -> XunDaiLi Proxy")
        # 10分钟更新一次
        url = "http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10"
        print("***begin -> XunDaiLi Proxy", url)
        response = requests.get(url=url, headers=self.headers, timeout=10)
        print("***run -> XunDaiLi Proxy", url, response)
        dic = json.loads(response.text)
        rows = dic["RESULT"]["rows"]
        items = []
        for row in rows:
            item = {}
            if row["anony"] == "高匿":
                item['ip'] = row["ip"] + ":" + row["port"]
                item['protocol'] = row["type"]
                items.append(item)
        print("*Finish -> XunDaiLi Proxy")
        return items

    # 5U代理 10min 1p
    def proxy__wuyou(self):
        print("*Start -> WuYou Proxy")
        url = "http://www.data5u.com/free/gngn/index.shtml"
        response = requests.get(url=url, headers=self.headers, timeout=10)
        print("***run -> WuYou Proxy", url, response)
        html = etree.HTML(response.text)
        rows = html.xpath("//div[@class='wlist']/ul/li/ul[@class='l2']")
        items = []
        for row in rows:
            item = {}
            ip = self.if_empty_list(row, "./span[1]/li/text()")
            port = self.if_empty_list(row, "./span[2]/li/text()")
            if ip and port:
                item['ip'] = ip + ":" + port
                item['protocol'] = self.if_empty_list(row, "./span[4]/li/a/text()")
                items.append(item)
        print("*Finish -> WuYou Proxy")
        return items

    # 快代理 12h 5p
    def proxy_kuai(self):
        print("*Start -> Kuai Proxy")
        base_url = "https://www.kuaidaili.com/free/inha/"
        start = 1
        end = 2
        def parse_info(offset):
            url = base_url + str(offset)
            print("***begin -> Kuai Proxy", url)
            response = requests.get(url=url, headers=self.headers, timeout=10)
            print("***run -> Kuai Proxy", url, response)

            # 解析页面过程不一样
            html = etree.HTML(response.text)
            rows = html.xpath("//table[@class='table table-bordered table-striped']/tbody/tr")
            items = []
            for row in rows:
                item = {}
                ip = self.if_empty_list(row, "./td[1]/text()")
                port = self.if_empty_list(row, "./td[2]/text()")
                if ip and port:
                    item['ip'] = ip + ":" + port
                    item['protocol'] = self.if_empty_list(row, "./td[4]/text()")
                    items.append(item)
            return items

        jobs = [gevent.spawn(parse_info, offset) for offset in range(start, end+1)]

        result = gevent.joinall(jobs)
        results = [ge_obj.value for ge_obj in result]
        origin = []
        for value in results:
            origin.extend(value)
        print("*Finish -> Kuai Proxy")
        return origin



c = CrawlProxy()
a = c.proxy__xici()
print(a)


# # 动态获取对象方法
# jobs = []
# for attr in dir(c):
#     if attr.startswith("proxy__"):
#         if attr not in []:
#             obj = getattr(c, attr, None)
#             jobs.append(gevent.spawn(obj))
# # 使用协程执行采集程序，并返回结果
# results = gevent.joinall(jobs)
#
# # 遍历采集的每个item
# for result in results:
#     for value in result.value:
#         print(value)





# test
# url = "https://www.kuaidaili.com/free/inha/1/"
# url = "http://www.xicidaili.com/nn/1"
# headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36", }
# response = requests.get(url=url, headers=headers)
# print(response)
# 如果是http请求使用协程，需要导入patch_socket
from gevent import monkey;monkey.patch_socket();monkey.patch_ssl()
import gevent
import requests
from lxml import etree
import time
import json
from bs4 import BeautifulSoup

"""
    exp_dic = {
    'exp_rows': 'exp',
    'exp_row_ip': 'exp',
    'exp_row_port': 'exp',
    'exp_row_protocol': 'exp',
}
"""


# 解析页面基础类
class BasePage(object):
    def __init__(self, base_url='', base_url_tail='', start=1, end=1, site_name="SiteName", exp_dic=None, sync_support=False):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/62.0.3202.62 Safari/537.36", }
        self.base_url = base_url
        self.base_url_tail = base_url_tail
        self.start = start
        self.end = end
        self.site_name = site_name
        self.exp_dic = exp_dic
        self.sync_support = sync_support

    # 使用xpath解析，如果解析为空就返回None，避免抛出异常
    def if_empty_list(self, dom, flag):
        lis = dom.xpath(self.exp_dic["exp_row_" + flag])
        if not lis:
            return None
        else:
            return lis[0].strip()

    def parse_page(self, offset):
        url = self.base_url + str(offset) + self.base_url_tail
        print("***begin -> {} Proxy: {}".format(self.site_name, url))
        response = requests.get(url=url, headers=self.headers, timeout=10)
        print("***begin -> {} Proxy: {} {}".format(self.site_name, url, response))
        return self.rule(response)

    # 解析规则
    def rule(self, response):
        html = etree.HTML(response.text)
        rows = html.xpath(self.exp_dic["exp_rows"])
        items = []
        for row in rows:
            item = {}
            ip = self.if_empty_list(row, "ip")
            port = self.if_empty_list(row, "port")
            if ip and port:
                item['ip'] = ip + ":" + port
                item['protocol'] = self.if_empty_list(row, "protocol").lower()
                items.append(item)
        return items

    # 顺序单任务抓取，针对同一个IP无法并发抓取的网站
    def order_crawl(self):
        origin = []
        for offset in range(self.start, self.end+1):
            items = self.parse_page(offset)
            origin.extend(items)
            time.sleep(1.5)
        print("*Finish -> {} Proxy".format(self.site_name))
        return origin

    # 异步抓取，使用协程提高采集性能
    def async_crawl(self):
        jobs = [gevent.spawn(self.parse_page, offset) for offset in range(self.start, self.end + 1)]
        result = gevent.joinall(jobs)
        results = [ge_obj.value for ge_obj in result]
        origin = []
        for value in results:
            origin.extend(value)
        print("*Finish -> {} Proxy".format(self.site_name))
        return origin

    # 运行，会根据配置选中是否异步
    def crawl(self):
        if self.start == '' or self.end == '':
            data = self.parse_page('')
        else:
            if self.sync_support:
                data = self.async_crawl()
            else:
                data = self.order_crawl()
        return data

    # 退出/清除占用内存
    def __del__(self):
        print("退出")


# 解析通用表格类型页面
class CommonTabelPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(CommonTabelPage, self).__init__(*args, **kwargs)

    # 解析规则
    def rule(self, response):
        html = etree.HTML(response.text)
        rows = html.xpath(self.exp_dic["exp_rows"])
        items = []
        for row in rows:
            item = {}
            ip = self.if_empty_list(row, "ip")
            port = self.if_empty_list(row, "port")
            if ip and port:
                item['ip'] = ip + ":" + port
                item['protocol'] = self.if_empty_list(row, "protocol").lower()
                items.append(item)
        return items
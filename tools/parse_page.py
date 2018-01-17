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


class ManyPage(object):
    def __init__(self, base_url, start, end, site_name, exp_dic, sync_support=False):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/62.0.3202.62 Safari/537.36", }
        self.base_url = base_url
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
        url = self.base_url + str(offset)
        print("***begin -> {} Proxy: {}".format(self.site_name, url))
        response = requests.get(url=url, headers=self.headers, timeout=10)
        print("***begin -> {} Proxy: {} {}".format(self.site_name, url, response))
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

    # 退出/清楚暂用内存
    def __del__(self):
        print("退出")


class ExtraAction(object):

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/62.0.3202.62 Safari/537.36", }
    @staticmethod
    def get_poxy(port_word):
        # print("start..")
        # print(port_word)
        # _, word = port_word.split(' ')
        num_list = []
        for item in port_word:
            num = 'ABCDEFGHIZ'.find(item)
            num_list.append(str(num))

        port = int("".join(num_list)) >> 0x3
        port = str(port)
        return port

    def crawl_quanwang(self):
        url = "http://www.goubanjia.com/free/gngn/index.shtml"
        r = requests.get(url=url, headers=self.headers)
        r = r.text

        # with open("./quanwang.html", "r") as f:
        #     r = f.read()

        soup = BeautifulSoup(r, "html.parser")
        ips = soup.tbody.findAll("tr")
        for ip in ips:
            b = ip.td
            c = b.contents
            m = ''
            for i in c:
                s = str(i)
                if "none" not in s:
                    if "port" in s:
                        mix = i.attrs['class'][1]
                        n = self.get_poxy(mix)
                    else:
                        n = i.string
                    if not n:
                        n = ''
                    m += n
            print(m)
# 如果是http请求使用协程，需要导入patch_socket
# from gevent import monkey;monkey.patch_socket();monkey.patch_ssl()
# import gevent
import requests
from lxml import etree
import time
import json

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
    def __init__(self, base_url='', base_url_tail='', start=1, end=1, site_name="SiteName", exp_dic=None, sync_support=False, cycle="2h", redis_store="test"):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/62.0.3202.62 Safari/537.36", }
        self.base_url = base_url
        self.base_url_tail = base_url_tail
        self.start = start
        self.end = end
        self.site_name = site_name
        self.exp_dic = exp_dic
        self.sync_support = sync_support
        self.cycle = cycle
        self.redis_store = redis_store

    # 使用xpath解析，如果解析为空就返回None，避免抛出异常
    def if_empty_list(self, dom, flag):
        lis = dom.xpath(self.exp_dic["exp_row_" + flag])
        if not lis:
            return None
        else:
            return lis[0].strip()

    def parse_page(self, offset):
        url = self.base_url + str(offset) + self.base_url_tail
        print("*Start -> {} Proxy: {}".format(self.site_name, url))

        while True:
            try:
                response = requests.get(url=url, headers=self.headers, timeout=10)
                if response.text == '':
                    raise Exception("响应为空")
                break
            except Exception as e:
                print(e)
                pass

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
            time.sleep(3)
        print("*Finish -> {} Proxy".format(self.site_name))
        return origin

    # # 异步抓取，使用协程提高采集性能
    # def async_crawl(self):
    #     jobs = [gevent.spawn(self.parse_page, offset) for offset in range(self.start, self.end + 1)]
    #     result = gevent.joinall(jobs)
    #     results = [ge_obj.value for ge_obj in result]
    #     origin = []
    #     for value in results:
    #         origin.extend(value)
    #     print("*Finish -> {} Proxy".format(self.site_name))
    #     return origin

    # 采集，会根据配置选中是否异步
    def crawl(self):
        if self.start == '' or self.end == '':
            data = self.parse_page('')
        else:
            if self.sync_support:
                # data = self.async_crawl()
                data = self.order_crawl()
            else:
                data = self.order_crawl()
        return data

    # 运行包括采集和储存
    def run(self, CONN_REDIS=None):
        while True:
            items = self.crawl()
            if CONN_REDIS:
                # 保存数据后开始休眠
                save_proxy_redis(CONN_REDIS, self.redis_store, items)
                wait(self.cycle)
                print("存入redis")
            else:
                return items

    # 退出/清除占用内存
    def __del__(self):
        print("{} Spider Exit".format(self.site_name))


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


# 把items保存到指定的redis集合里面
def save_proxy_redis(CONN_REDIS, redis_store, items):

    for proxy in items:
        if proxy["protocol"] in ["http", "http,https", "https,http"]:
            CONN_REDIS.rpush(redis_store+"http", proxy["ip"])
        elif proxy["protocol"] in ["sock", "socks", "socket", "socks4/5", "socks4", "socks5"]:
            CONN_REDIS.rpush(redis_store + "socks", proxy["ip"])
        else:
            CONN_REDIS.rpush(redis_store + "https", proxy["ip"])


# 根据规则睡眠采集脚本
def wait(string):
    if string.endswith("h"):
        num = string.replace("h", "")
        print("等待%s小时" % num)
        time.sleep(int(num)*3600)
    elif string.endswith("min"):
        num = string.replace("min", "")
        print("等待%s分钟" % num)
        time.sleep(int(num)*60)
    else:
        raise TypeError("参数异常")


def test_proxy(proxy):

    if proxy["protocol"] in ["http", "http,https", "https,http"]:
        proxies = {"http": proxy["ip"]}
    else:
        proxies = {"https": proxy["ip"]}

    url = "http://httpbin.org/ip"
    print(proxies)

    while True:
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            print(response.status_code)
            if response.status_code == '200':
                print(proxies, "sucess!")
                break
        except:
            pass

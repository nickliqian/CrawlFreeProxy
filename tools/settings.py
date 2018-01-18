from tools.common import CommonTabelPage
from tools.special import QuanWang


# 快代理 带CONN_REDIS参数就会循环的采集并存入redis，如果不带就会返回单次采集的集合 [{}, {}, ...]
def proxy__kuai(CONN_REDIS=None):
    base_url = "https://www.kuaidaili.com/free/inha/"
    base_url_tail = ''
    start = 1
    end = 10
    site_name = "Kuai"
    cycle = '6h'  # 5p
    sync_support = False
    redis_store = "freeProxy:BeforeVerify"
    exp_dic = {
        "exp_rows": "//table[@class='table table-bordered table-striped']/tbody/tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[4]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support, cycle, redis_store)
    items = Spider.run(CONN_REDIS)
    return items


# 西刺代理
def proxy__xici(CONN_REDIS=None):
    base_url = "http://www.xicidaili.com/nn/"
    base_url_tail = ''
    start = 1
    end = 10
    site_name = "XiCi"
    cycle = '6h'  # 5p
    # 支持异步
    sync_support = False
    redis_store = "freeProxy:BeforeVerify"
    exp_dic = {
        "exp_rows": "//table[@id='ip_list']//tr[@class]",
        "exp_row_ip": "./td[2]/text()",
        "exp_row_port": "./td[3]/text()",
        "exp_row_protocol": "./td[6]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support, cycle, redis_store)
    items = Spider.run(CONN_REDIS)
    return items


# 年少代理
def proxy__nianshao(CONN_REDIS=None):
    base_url = "http://www.nianshao.me/?page="
    base_url_tail = ''
    start = 1
    end = 20
    site_name = "NiaoShao"
    cycle = '3h'  # 10p
    sync_support = False
    redis_store = "freeProxy:BeforeVerify"
    exp_dic = {
        "exp_rows": "//table[@class='table']/tbody/tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[5]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support, cycle, redis_store)
    items = Spider.run(CONN_REDIS)
    return items


# 云代理
def proxy__ip3366(CONN_REDIS=None):
    base_url = "http://www.ip3366.net/free/?stype=3&page="
    base_url_tail = ''
    start = 1
    end = 10
    site_name = "IP3366"
    cycle = '6h'  # 5p
    sync_support = False
    redis_store = "freeProxy:BeforeVerify"
    exp_dic = {
        "exp_rows": "//table[@class='table table-bordered table-striped']/tbody/tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[4]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support, cycle, redis_store)
    items = Spider.run(CONN_REDIS)
    return items


# IP海
def proxy__iphai(CONN_REDIS=None):
    base_url = "http://www.iphai.com/free/ng"
    base_url_tail = ''
    start = ''
    end = ''
    site_name = "IP3366"
    cycle = '6h'  # 1p
    sync_support = False
    redis_store = "freeProxy:BeforeVerify"
    exp_dic = {
        "exp_rows": "//table//tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[4]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support, cycle, redis_store)
    items = Spider.run(CONN_REDIS)
    return items


# 5U代理 10min 1p
def proxy__wuyou(CONN_REDIS=None):
    base_url = "http://www.data5u.com/free/gngn/index.shtml"
    base_url_tail = ''
    start = ''
    end = ''
    site_name = "WuYou"
    cycle = '10min'  # 1p
    sync_support = False
    redis_store = "freeProxy:BeforeVerify"
    exp_dic = {
        "exp_rows": "//div[@class='wlist']/ul/li/ul[@class='l2']",
        "exp_row_ip": "./span[1]/li/text()",
        "exp_row_port": "./span[2]/li/text()",
        "exp_row_protocol": "./span[4]/li/a/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support, cycle, redis_store)
    items = Spider.run(CONN_REDIS)
    return items


# 全网代理 10min 5
def proxy__quanwang(CONN_REDIS=None):
    Spider = QuanWang(start=1, end=20, cycle="10min")  # 5p
    items = Spider.run(CONN_REDIS)
    return items

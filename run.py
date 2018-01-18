from tools.common import CommonTabelPage
from tools.special import QuanWang


# 快代理
def proxy_kuai():
    base_url = "https://www.kuaidaili.com/free/inha/"
    base_url_tail = ''
    start = 1
    end = 2
    site_name = "Kuai"
    time = '12h'  # 5p
    sync_support = False
    exp_dic = {
        "exp_rows": "//table[@class='table table-bordered table-striped']/tbody/tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[4]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support)
    items = Spider.crawl()
    [print(i) for i in items]


# 西刺代理
def proxy_xici():
    base_url = "http://www.xicidaili.com/nn/"
    base_url_tail = ''
    start = 1
    end = 2
    site_name = "XiCi"
    time = '12h'  # 5p
    # 支持异步
    sync_support = False
    exp_dic = {
        "exp_rows": "//table[@id='ip_list']//tr[@class]",
        "exp_row_ip": "./td[2]/text()",
        "exp_row_port": "./td[3]/text()",
        "exp_row_protocol": "./td[6]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support)
    items = Spider.crawl()
    [print(i) for i in items]


# 年少代理
def proxy_nianshao():
    base_url = "http://www.nianshao.me/?page="
    base_url_tail = ''
    start = 1
    end = 2
    site_name = "NiaoShao"
    time = '2h'  # 10p
    sync_support = False
    exp_dic = {
        "exp_rows": "//table[@class='table']/tbody/tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[5]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support)
    items = Spider.crawl()
    [print(i) for i in items]


# 云代理
def proxy_ip3366():
    base_url = "http://www.ip3366.net/free/?stype=1"
    base_url_tail = ''
    start = 1
    end = 2
    site_name = "IP3366"
    time = '12h'  # 5p
    sync_support = False
    exp_dic = {
        "exp_rows": "//table[@class='table table-bordered table-striped']/tbody/tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[4]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support)
    items = Spider.crawl()
    [print(i) for i in items]

# IP海
def proxy_iphai():
    base_url = "http://www.iphai.com/free/ng"
    base_url_tail = ''
    start = ''
    end = ''
    site_name = "IP3366"
    time = '6h'  # 1p
    sync_support = False
    exp_dic = {
        "exp_rows": "//table//tr",
        "exp_row_ip": "./td[1]/text()",
        "exp_row_port": "./td[2]/text()",
        "exp_row_protocol": "./td[4]/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support)
    items = Spider.crawl()
    [print(i) for i in items]

# 5U代理 10min 1p
def proxy_wuyou():
    base_url = "http://www.data5u.com/free/gngn/index.shtml"
    base_url_tail = ''
    start = ''
    end = ''
    site_name = "WuYou"
    time = '10min'  # 1p
    sync_support = False
    exp_dic = {
        "exp_rows": "//div[@class='wlist']/ul/li/ul[@class='l2']",
        "exp_row_ip": "./span[1]/li/text()",
        "exp_row_port": "./span[2]/li/text()",
        "exp_row_protocol": "./span[4]/li/a/text()",
    }
    Spider = CommonTabelPage(base_url, base_url_tail, start, end, site_name, exp_dic, sync_support)
    items = Spider.crawl()
    [print(i) for i in items]


# 全网代理 10min 5
def proxy_quanwang():
    start = 1
    end = 2
    time = '10min'  # 5p
    Spider = QuanWang(start, end)
    items = Spider.crawl()
    [print(i) for i in items]


if __name__ == '__main__':

    proxy_kuai()
    # proxy_xici()
    # proxy_nianshao()
    # proxy_ip3366()
    # proxy_iphai()
    # proxy_wuyou()
    # proxy_quanwang()


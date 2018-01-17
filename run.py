from tools.parse_page import ManyPage


# 快代理
def kuai():
    base_url = "https://www.kuaidaili.com/free/inha/"
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
    m = ManyPage(base_url, start, end, site_name, exp_dic, sync_support)
    a = m.crawl()
    print(a)


# 西刺代理
def xici():
    base_url = "http://www.xicidaili.com/nn/"
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
    m = ManyPage(base_url, start, end, site_name, exp_dic, sync_support)
    a = m.crawl()
    print(a)


# 年少代理
def nianshao():
    base_url = "http://www.nianshao.me/?page="
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
    m = ManyPage(base_url, start, end, site_name, exp_dic, sync_support)
    a = m.crawl()
    print(a)


# 云代理
def ip3366():
    base_url = "http://www.ip3366.net/free/?stype=1"
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
    m = ManyPage(base_url, start, end, site_name, exp_dic, sync_support)
    a = m.crawl()
    print(a)

# IP海
def iphai():
    base_url = "http://www.iphai.com/free/ng"
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
    m = ManyPage(base_url, start, end, site_name, exp_dic, sync_support)
    a = m.crawl()
    print(a)

# 5U代理 10min 1p
def wuyou():
    base_url = "http://www.data5u.com/free/gngn/index.shtml"
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
    m = ManyPage(base_url, start, end, site_name, exp_dic, sync_support)
    a = m.crawl()
    print(a)


wuyou()
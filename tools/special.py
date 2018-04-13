from bs4 import BeautifulSoup
from tools.common import BasePage
import time


# 全网代理 扩展自定义函数应对反爬措施
class QuanWang(BasePage):
    def __init__(self, *args, **kwargs):
        super(QuanWang, self).__init__(*args, **kwargs)
        self.base_url = "http://www.goubanjia.com/free/gngn/index"
        self.base_url_tail = ".shtml"
        self.site_name = "QuanWang"
        self.sync_support = False
        self.cycle = '10min'
        self.redis_store = "freeProxy:BeforeVerify"

    # 端口加密破解
    @staticmethod
    def get_poxy(port_word):
        num_list = []
        for item in port_word:
            num = 'ABCDEFGHIZ'.find(item)
            num_list.append(str(num))

        port = int("".join(num_list)) >> 0x3
        port = str(port)
        return port

    # 规则重写
    def rule(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        while True:
            try:
                rows = soup.tbody.findAll("tr")
                break
            except Exception as e:
                print(e, response.url)
                with open("./test/quanwangerror.html", "w") as f:
                    f.write(response.url)
                    f.write(response.text)
                time.sleep(300)
        items = []
        for row in rows:
            try:
                item = {}
                ip_tags = row.td.contents
                item['protocol'] = row.findAll("td")[2].string
                full_ip = ''
                for tag in ip_tags:
                    tag_string = str(tag)
                    if "none" not in tag_string:
                        if "port" in tag_string:
                            hash_word = tag.attrs['class'][1]
                            n = self.get_poxy(hash_word)
                        else:
                            n = tag.string
                        n = '' if not n else n
                        full_ip += n
                item['ip'] = full_ip
                items.append(item)
            except Exception as e:
                print(e)
                pass
        return items

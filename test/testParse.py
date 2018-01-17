import requests
from bs4 import BeautifulSoup


url = "http://www.goubanjia.com/free/gngn/index.shtml"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",}

r = requests.get(url=url, headers=headers)
r = r.text

# with open("./quanwang.html", "r") as f:
#     r = f.read()

soup = BeautifulSoup(r, "html.parser")
ips = soup.tbody.findAll("tr")

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

for ip in ips:
    b = ip.td
    c = b.contents
    m = ''
    for i in c:
        s = str(i)
        if "none" not in s:
            if "port" in s:
                mix = i.attrs['class'][1]
                n = get_poxy(mix)
            else:
                n = i.string
            if not n:
                n = ''
            m += n
    print(m)


"""
for ip in ips:
    # ip = ips[0].td
    all = list(ip.td.childGenerator())
    print(type(all[0]))
    # print(all)
    # s = ''
    # for i in all:
    #     if "display: none" not in str(i):
    #         ss = i.string if i.string else ''
    #         s += ss
    # print(s)
"""




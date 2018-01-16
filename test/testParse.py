import requests
from bs4 import BeautifulSoup


url = "http://www.goubanjia.com/free/index1.shtml"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",}

r = requests.get(url=url, headers=headers)

soup = BeautifulSoup(r.text, "lxml")
ips = soup.tbody.findAll("tr")
for ip in ips:
    # ip = ips[0].td
    all = list(ip.td.childGenerator())
    s = ''
    for i in all:
        if "display: none" not in str(i):
            ss = i.string if i.string else ''
            s += ss
    print(s)


"""
118.193.107.146:80      
175.8.85.61:8118        
94.141.244.132:8081     
128.199.167.199:80      
27.40.151.128:61234     
221.217.49.76:9000      
60.163.121.158:9000     
202.137.25.53:3128      
103.233.157.236:53281       
222.186.45.60:63064     
51.255.141.15:80        
86.57.139.127:3128      
39.134.146.118:8088     
111.155.116.210:8123        
216.59.137.117:3838     
"""
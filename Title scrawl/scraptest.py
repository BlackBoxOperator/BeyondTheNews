"""
Program : 新聞標題爬蟲程式
Status  : 目前還在爬，估計要一到兩天才能爬完
執行時間滿久的，應該可以想辦法優化
"""

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError

session = requests.Session()
#建構一個假的使用電腦，模擬成使用者，不然會被新聞網站阻擋
headers = {
        "User-Agent":"Yuancircle/3.0(HP pavilion ce 2003tx new;Intel)"
        "windowsWebkit 537.36 (KHTML,like Gecko) Chrome",
        "Accept":"text/html,application/xhtml+xml,application/xml;"
        "q=0.9,imge/webp,*/*;q=0.8"
        }
#將每則新聞建立一個dictionary，key = newsID,value = URL
links = open("NC_1.csv","r")
ary = links.read().splitlines()
jary = ",".join(ary)
x = jary.split(",")
dic = dict()
#建立字典
for index in range(0,len(x),2):
    dic[x[index]] = x[index+1]


#主要爬行程序，利用dictionary的 URL value 進行 request.
for (name,html) in dic.items():
    try:
        if html[0] != 'h':
            continue
        html1 = session.get(html,headers=headers)
    except HTTPError as e:
        strn = "None"
    try:
        bs = BeautifulSoup(html1.text,"html.parser")
        strn = str(bs.find("title"))
    except AttributeError as e:
        strn = "None"
    print(name,strn)

#print後利用pipline導入到title檔案

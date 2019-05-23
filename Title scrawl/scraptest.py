"""
Program : 新聞標題爬蟲程式
Status  : 目前還在爬，估計要一到兩天才能爬完
執行時間滿久的，應該可以想辦法優

做了一些修正,改善request 時間過長導致程式崩潰的問題，但是title出現None
"""
import urllib.request as urllib
from bs4 import BeautifulSoup
from urllib.error import HTTPError

headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)"
        }

links = open("NC_1.csv","r")
ary = links.read().splitlines()
jary = ",".join(ary)
x = jary.split(",")
dic = dict()
for index in range(23116,len(x),2):
    dic[x[index]] = x[index+1]

for (name,html) in dic.items():
    try:
        if html[0] != 'h':
            continue
        req = urllib.Request(url=html,headers=headers)
        html1 = urllib.urlopen(req,timeout=5)
    except Exception as e:
        try:
            html1 = urllib.urlopen(req,timeout=10)
        except Exception as e:
            strn = "None"
    try:
        bs = BeautifulSoup(html1.read(),"html.parser")
        strn = str(bs.find("title"))
    except AttributeError as e:
        strn = "None"
    print(name,strn)

#print後利用pipline導入到title檔案

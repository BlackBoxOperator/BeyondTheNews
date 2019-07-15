# AIdea - BeyondTheNews

[Project Introduction Link](http://wm5.nccu.edu.tw/base/10001/course/10021115/content/proj03/index.html)

[Contest Link](https://aidea-web.tw/topic/b6abbf14-2d60-456c-8cbe-34fdfcd58967)

## tools

#### stopwords

有些 stop words 可能會影響結果，如 `不`，應該會影響立場的分類。

- [chinese stop words](https://github.com/goto456/stopwords)
- [chinese stop words](https://www.ranks.nl/stopwords/chinese-stopwords)
- [chinese stop words](https://countwordsfree.com/stopwords/chinese)
- [chinese stop words](https://blog.csdn.net/shijiebei2009/article/details/39696571)
- [中文 NLP 資源（內含 stopwords）](https://github.com/tomlinNTUB/Python-in-5-days/blob/master/10-2%20%E4%B8%AD%E6%96%87%E6%96%B7%E8%A9%9E-%E7%A7%BB%E9%99%A4%E5%81%9C%E7%94%A8%E8%A9%9E.md)

## approachs

#### Vector Space Model


#### Language Model


#### Support Vector Machine


## ideas

- 新聞分類（如蘋果：總覽 熱門 要聞 娛樂 國際 財經 副刊 體育 地產 論壇與專欄）重爬 然後歸類。
   - 把所有新聞來源網站找出來查出所有分類聯集
   - 必要時直接從分類 total 下去爬

## scripts

- `extract_domain.py`
   將 `NC_1.csv` URL 的 domain parse 出來，並 show 出 invalid URLs

## summary

資料中有些非法的 URLs ：
```
/appledaily/article/adcontent/20170114/37518814/
/appledaily/article/adcontent/20170817/37750863/
/appledaily/article/adcontent/20161223/37494145/
/appledaily/article/adcontent/20161101/37432052/
/appledaily/article/adcontent/20170414/37616791/
/appledaily/article/adcontent/20170729/37730727/
/appledaily/article/adcontent/20161021/37424082/
/appledaily/article/adcontent/20170803/37736089/
/appledaily/article/adcontent/20170721/37722716/
/appledaily/article/adcontent/20171208/37868026/
/appledaily/article/adcontent/20170526/37662239/
/appledaily/article/adcontent/20170715/37715548/
```
其在 url2content.\* 的內容為：
```
《蘋果》論壇歡迎投稿，一經錄用將附上稿酬。若一稿多投，本社將不支付稿酬。本報有刪修權，網站刊登不另計酬；三日未見報請自行處理，不另通知。
請寄public@appledaily.com.tw，來稿請附真實姓名、身分證字號、職業、電話、銀行帳戶和通訊地址。                                           
更多的專欄文章，請見蘋果網站《蘋論陣線》：
http://www.appledaily.com.tw/realtimenews/forum
```

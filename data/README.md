# AIdea - BeyondTheNews - Data

please download all data from [google drive](https://drive.google.com/open?id=18dAtXYPi02UxMhyUkZoG-VafFUdyX793)

google drive:
   - dicts.rar: dict.txt, simple_dict.txt, wdict.txt, simple_wdict.txt
   - stopwrods.rar: stopword.txt, simple_stopword.txt
   - NC_1.rar: NC_1.csv
   - NC_2.rar: NC_2.csv
   - title.rar: title.json (NC_1's doc title)
   - NC1_content.rar: url2content.json (NC_1's content)
   - NC2_content.rar: idx2content.csv (NC_2's title and content)

other corpus:
  - [aclclp](http://www.aclclp.org.tw/member/corp_c.php)
  - [iis](http://asbc.iis.sinica.edu.tw/)
  - [icorpus](http://asbc.iis.sinica.edu.tw/)
  - [scidm](https://scidm.nchc.org.tw/dataset/nchc_2019_te_02)

## 部分新聞語料庫（NC-1）

NC_1.csv：包含 News_Index、News_URL 兩個欄位，News_Index 表示新聞編號，News_URL 是對應的新聞連結，參賽隊伍需自行下載新聞，並且只能以「新聞標題」和「新聞文字內文」作爲檢索依據。

| News_Index|News_URL |
| :---: | :---: |
| news_000001| http://www.chinatimes.com/newspapers/20150108001507-260107 |
| news_000002| http://tw.sports.appledaily.com/daily/20110623/33479530/ |
| ... | ... |
| news_100000 | http://tw.news.appledaily.com/headline/daily/20160311/37103743/ |

## 測試查詢題目（QS-1）

QS_1.csv：包含 Query_Index、Query 兩個欄位，Query_Index 為測試查詢題目的編號，Query 為測試查詢題目。

| Query_Index | Query |
| :---: | :---: |
| q_01 | 通姦在刑法上應該除罪化 |
| q_02 | 應該取消機車強制待轉或二段式左轉 |
| ... | ... |
| q_20 | 反對旺旺中時併購中嘉 |

## 訓練標記語料（TD）

TD.csv：包含 Query、News_Index、Relevance 三個欄位，Query 為訓練查詢題目，News_Index 為新聞編號，Relevance 為相關程度，相關程度 0、1、2、3 分別代表不相關 (0)、部分相關 (1)、相關 (2)、非常相關 (3)。Query 必定含有立場，若某一文件之內容與 Query 內的議題有關，但立場與 Query 不一致，仍視為不相關 (0)。

|Query | News_Index | Relevance |
| :---: | :---: | :---: |
|贊成流浪動物零撲殺 | news_000109 | 3 |
|核四應該啟用 | news_000156 | 1 |
|... | ... | ... |
|遠雄大巨蛋工程應停工或拆除 | news_000684 | 0 |
|拒絕公投通過門檻下修 | news_000091 | 2 |

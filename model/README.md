# 排序模型、上傳檔案及成績紀錄

還可嘗試的方向：
- n-gram
- 情緒辭典
- word embedding
   - [pre train wrod2vec model](https://drive.google.com/open?id=1brDVqxu9osM3p1vva2JpIUQ_15IvKOZy)
- [同義詞搜尋系統](https://120.127.233.228/word2vec/)
- nn

| model | submit |    成績   |         日期        | 備註 |
| :---: | :----: | :-------: | :-----------------: | :--: |
| 0.py  | 0.csv  | 0.1720243 | 2019/06/13 17:53:20 | 使用 `jieba_search 斷詞, tf-idf vector 以及 cos similarity, 斷詞僅留中文 |
| 1.py  | 1.csv  | 0.0763763 | 2019/06/13 19:49:46 | 同 0.py, 使用 `jiebal.cut(all=True)` 斷詞 |
| 2.py  | 2.csv  | 0.0245111 | 2019/06/13 20:34:37 | 使用 title, cut all 僅留中文|
| 3.py  | 3.csv  | 0.1717637 | 2019/06/14 02:50:45 | 同 0.py 但加了 ECFA 僅留中文|
| 4.py  | 4.csv  | 0.1719835 | 2019/06/14 03:02:52 | 同 0.py 但把 "不 ??" 連起來|
| 5.py  | 5.csv  | 0.1859260 | 2019/06/14 10:45:23 | 同 0.py 但改成 bm25 |
| 6.py  | 6.csv  | 0.1869177 | 2019/06/14 17:19:21 | 同 5.py 加上 query 字典 |
| 7.py  | 7.csv  | 0.1919284 | 2019/06/14 22:58:53 | 同 6.py 加上 Relevance Feedback(query + 0.5 R1) |
| 8.py  | 8.csv  | 0.1837587 | 2019/06/14 23:29:11 | 同 6.py 加上 custom query |
| 9.py  | 9.csv  | 0.1972519 | 2019/06/14 23:41:07 | 同上上 Relevance Feedback(query + 0.5 R1 + 0.25 R2) |
| 10.py | 10.csv | 0.2014145 | 2019/06/14 23:46:09 | 同上 Relevance Feedback(query + 0.[75,5,25] R[1,2,3]) |
| 11.py | 11.csv | 0.2034738 | 2019/06/15 00:04:15 | 同上 Relevance Feedback(query + 0.[8,6,4,2,1] R[1,2,3,4,5]|
| 12.py | 12.csv | 0.2060819 | 2019/06/15 00:15:18 | 同上 Relevance Feedback(query + [i=1..9 (1-0.1 * i) Ri] + 0.1 R10 ) |
| 13.py | 13.csv | 0.2137932 | 2019/06/15 00:21:19 | 同上 Relevance Feedback(query + [i=1..10 0.5 Ri]) |
| 14.py | 14.csv | 0.2204961 | 2019/06/15 00:28:27 | 同上 Relevance Feedback(query + [i=1..30 0.5 Ri]) |
| 15.py | 15.csv | 0.2245856 | 2019/06/15 00:40:50 | 同上 Relevance Feedback(query + [i=1..50 0.5 Ri]) |
| 16.py | 16.csv | 0.2276242 | 2019/06/15 00:48:34 | 同上 Relevance Feedback(query + [i=1..100 0.5 Ri])|
| 17.py | 17.csv | 0.2292303 | 2019/06/15 01:30:41 | 同上 Relevance Feedback, 加了 title|
| 18.py | 18.csv | 0.2293031 | 2019/06/15 03:44:47 | 同上 but reToken with larger dict |
| 19.py | 19.csv | 0.2566023 | 2019/06/17 10:17:55 | 同 18.py 手動加 '陸生 中生 大陸' 進 query |
| 20.py | 20.csv | 0.2566023 | 2019/06/17 10:17:55 | 同 19.py 手動加 '證所' 進 dict |
| 21.py | 21.csv | 0.2577842 | 2019/06/17 21:21:16 | 同 20.py Relevance Feedback 2 stage(50, 100) |
| 22.py | 22.csv | 0.2587751 | 2019/06/17 21:40:14 | 同 20.py Relevance Feedback n stage(20, 40..80) |
| 23.py | 23.csv | 0.2609018 | 2019/06/17 21:49:18 | 同 20.py Relevance Feedback n stage(20, 40..100), doc title * 2 |
| 24.py | 24.csv | 0.2509281 | 2019/06/17 21:59:42 | 同 20.py Relevance Feedback n stage(20, 40..100), doc title * 5 |
| 25.py | 25.csv | 0.2591175 | 2019/06/17 22:09:57 | 同 20.py Relevance Feedback n stage(20, 40..100), doc title * 3 |
| 26.py | 26.csv | 0.2571164 | 2019/06/17 22:26:24 | 同 20.py Relevance Feedback n stage(20, 40..100) |
| 27.py | 27.csv | 0.2587824 | 2019/06/17 23:28:03 | 同 20.py Relevance Feedback n stage(20, 40..120), doc title * 2 |
| 28.py | 28.csv | 0.2605769 | 2019/06/18 00:02:00 | 同 20.py Relevance Feedback n stage(10, 20..100), doc title * 2 |
| 29.py | 29.csv | 0.2663411 | 2019/06/23 00:58:07 | 同 26.py Relevance Feedback += score(word2Vec)|
| 30.py | 30.csv | 0.2668813 | 2019/06/24 04:02:06 | 同 23.py Relevance Feedback += score(word2Vec)|
| 31.py | 31.csv | 0.2677088 | 2019/06/25 02:14:04 | 同 30.py Relevance Feedback += score(word2Vec_wikiPre_news_d100)|
| 32.py | 32.csv | 0.2712938 | 2019/06/25 00:16:59 | 同 30.py Relevance Feedback += score(word2Vec_news_d200)|
| 33.py | none | non | none | explosion |


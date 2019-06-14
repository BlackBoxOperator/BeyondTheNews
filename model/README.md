# 排序模型、上傳檔案及成績紀錄

還可嘗試的方向：
- doc 加上 title
- n-gram
- 情緒辭典
- word embedding
- nn

| model | submit |   成績   |         日期        | 備註 |
| :---: | :----: | :------: | :-----------------: | :--: |
| 0.py  |0.csv   |0.1720243 | 2019/06/13 17:53:20 | 使用 `jieba_search 斷詞, tf-idf vector 以及 cos similarity, 斷詞僅留中文 |
| 1.py  |1.csv   |0.0763763 | 2019/06/13 19:49:46 | 同 0.py, 使用 `jiebal.cut(all=True)` 斷詞 |
| 2.py  |2.csv   |0.0245111 | 2019/06/13 20:34:37 | 使用 title, cut all 僅留中文|
| 3.py  |3.csv   |0.1717637 | 2019/06/14 02:50:45 | 同 0.csv, 但加了 ECFA 僅留中文|
| 4.py  |4.csv   |0.1719835 | 2019/06/14 03:02:52 | 同 0.csv, 但把 "不 ??" 連起來|
| 5.py  |5.csv   |0.1859260 | 2019/06/14 10:45:23 | 同 0.csv 但改成 bm25 |
| 6.py  |6.csv   |0.1869177 | 2019/06/14 17:19:21 | 同 5.csv 加上 query 字典 |
| 7.py  |7.csv   |0.1919284 | 2019/06/14 22:58:53 | 同 6.csv 加上 Relevance Feedback(query + 0.5 R1) |
| 8.py  |8.csv   |0.1837587 | 2019/06/14 23:29:11 | 同 6.csv 加上 custom query |
| 9.py  |9.csv   |0.1972519 | 2019/06/14 23:41:07 | 同上上 Relevance Feedback(query + 0.5 R1 + 0.25 R2) |
| 10.py |10.csv  |0.2014145 | 2019/06/14 23:46:09 | 同上 Relevance Feedback(query + 0.75 R1 + 0.5 R2 + 0.25 R3) |
| 11.py |11.csv  |0.2034738 | 2019/06/15 00:04:15 | 同上 Relevance Feedback(query + 0.8 R1 + 0.6 R2 + 0.4 R3 + 0.2 R4 + 0.1 R5) |
| 12.py |12.csv  |0.2060819 | 2019/06/15 00:15:18 | 同上 Relevance Feedback(query + [i=1..9 (1-0.1 * i) Ri] + 0.1 R10 ) |
| 13.py |13.csv  |0.2137932 | 2019/06/15 00:21:19 | 同上 Relevance Feedback(query + [i=1..10 0.5 Ri]) |
| 14.py |14.csv  |0.2204961 | 2019/06/15 00:28:27 | 同上 Relevance Feedback(query + [i=1..30 0.5 Ri]) |
| 15.py |15.csv  |0.2245856 | 2019/06/15 00:40:50 | 同上 Relevance Feedback(query + [i=1..50 0.5 Ri]) |
| 16.py |16.csv  |0.2276242 | 2019/06/15 00:48:34 | 同上 Relevance Feedback(query + [i=1..100 0.5 Ri])|
| 17.py |17.csv  |0.2292303 | 2019/06/15 01:30:41 | 同上 Relevance Feedback, 加了 title|



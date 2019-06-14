# 排序模型

| 檔名 | 備註 |
| :--: | :--: |
| 0.py | 使用 `jieba_search 斷詞, tf-idf vector 以及 cos similarity |
| 1.py | 使用 `jiebal.cut(all=True)` 斷詞, tf-idf vector 以及 cos similarity |
| 2.py | 僅使用 title 作為 corpus，用 `jiebal.cut(all=True)` + cos similarity |
| 3.py | 同 0.csv, 但加了 ECFA 僅留中文 |
| 4.py | 同 0.csv, 但把 "不 ??" 連起來 |
| 5.py | 同 0.csv, 但加入 bm25 |
| 6.py | 同 5.csv 加上字典 |

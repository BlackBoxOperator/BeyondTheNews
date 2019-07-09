from tqdm import *
import numpy as np
import time, jieba, os, json, csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
from score_functions import twostage
from itertools import starmap
from bm25 import BM25Transformer

QS_1 = """通姦 刑法 除罪 除罪化
機車 二段 段式 二段式 左轉 待轉
博弈 特區 台灣 合法 合法化
中華 航空 空服員 罷工 合理
性交 交易 性交易 合法 合法化
ECFA 早收 清單 達到 預期 成效 海峽 兩岸 經濟
減免 證所稅
中油 觀塘 興建 第三 天然 天然氣 接收 接收站
中國 學生 納入 健保
臺灣 中小 中小學 含 高職 專科 服儀 規定 含 髮 襪 鞋 給予 學生 自主
使用 加密 貨幣
學雜費 調漲
政府 舉債 發展 前瞻 建設 計畫
電競 列入 體育 競技
台鐵 東移 徵收 徵收案
陳 前 總統 保外 就醫 水扁 扁
年金 改革  公教 軍公教 月退 優存 利率 十八 趴
動物 實驗
油價 凍漲 緩漲
旺旺 中時 併購 中嘉
通姦 刑法 應該 除罪 除罪化 同意 贊成 支持
應該 取消 機車 強制 二段 段式 二段式 左轉 待轉 同意 贊成 支持
支持 博弈 特區 台灣 合法 合法化 同意 贊成
中華 航空 空服員 罷工 合理
性交 交易 性交易 應該 合法 合法化 同意 贊成 支持
ECFA 早收 清單 達到 預期 成效 海峽 兩岸 經濟
應該 減免 證所稅 同意 贊成 支持
贊成 中油 觀塘 興建 第三 天然 天然氣 接收 接收站
支持 中國 學生 納入 健保 應該 同意 贊成
支持 臺灣 中小 中小學 含 高職 專科 服儀 規定 含 髮 襪 鞋 給予 學生 自主 應該 同意 贊成
不 支持 使用 加密 貨幣 不 應該 不 同意 不 贊成 反對
不 支持 學雜費 調漲 不 應該 不 同意 不 贊成 反對
同意 政府 舉債 發展 前瞻 建設 計畫 應該 贊成 支持
支持 電競 列入 體育 競技 應該 贊成 同意
反對 台鐵 東移 徵收 徵收案 不 支持 不 同意 不 應該
支持 陳 前 總統 保外 就醫 應該 同意 贊成 水扁 扁
年金 改革 應 取消 或應 調降 公教 軍公教 月退 優存 利率 十八 趴
同意 動物 實驗 贊成 支持 應該
油價 應該 凍漲 緩漲 贊成 支持
反對 旺旺 中時 併購 中嘉 不 應該 不 支持 不 贊成"""

stopwordFile = os.path.join('..', 'data', "stopword.txt")
outputFile = os.path.join('..', 'submit', 'current.csv')

cut_method = jieba.cut_for_search
tokenFile = os.path.join('..', 'tokens', 'search_dict_token.txt')
tokeyFile = os.path.join('..', 'tokens', 'search_dict_tokey.txt')
queryDictFile = os.path.join('..', 'data', 'dict.txt')

jieba.load_userdict(queryDictFile)

if __name__ == '__main__':

    stopwords = open(stopwordFile, 'r').read().split()
    queries = QS_1.split('\n')
    two_stage_queries = [(i + 1, f, s) for i, (f, s)
                                in enumerate(zip(queries[:20], queries[20:]))]

    trim = lambda f: [t.strip() for t in f if t.strip()]
    token = trim(open(tokenFile).read().split('\n'))#[:5000]#[:301]
    tokey = trim(open(tokeyFile).read().split('\n'))#[:5000]#[:301]

    if len(token) != len(tokey):
        print('token len sould eq to tokey len')
        exit(0)

    bm25 = BM25Transformer()
    vectorizer = TfidfVectorizer()
    doc_tf = vectorizer.fit_transform(tqdm(token))

    bm25.fit(doc_tf)
    doc_bm25 = bm25.transform(doc_tf)

    print('\ncorpus vector space - ok\n')

    with open(outputFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['Query_Index'] + ['Rank_{:03d}'.format(i) for i in range(1, 301)]
        writer.writerow(headers)

        for i, fq, sq in tqdm(two_stage_queries):
            print('First Query: ' + fq)
            qry_tf = vectorizer.transform([fq])
            qry_bm25 = bm25.transform(qry_tf)

            sims = cosine_similarity(qry_bm25, doc_bm25)[0]
            ranks = [(t, v) for (v, t) in zip(sims, tokey)]
            ranks.sort(key=lambda e: e[-1], reverse=True)

            sub = [tokey.index(r[0]) for r in ranks[:600]]
            sub_tokey = [r[0] for r in ranks[:600]]

            print('Second Query: ' + sq)
            qry_tf = vectorizer.transform([sq])
            qry_bm25 = bm25.transform(qry_tf)

            sims = cosine_similarity(qry_bm25, doc_bm25[sub])[0]
            ranks = [(t, v) for (v, t) in zip(sims, sub_tokey)]
            ranks.sort(key=lambda e: e[-1], reverse=True)

            entry = ['q_{:02d}'.format(i)] + [e[0] for e in ranks[:300]]
            writer.writerow(entry)

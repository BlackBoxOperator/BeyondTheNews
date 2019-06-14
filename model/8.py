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

queryFile = os.path.join('..', 'data', 'custom_query.txt')
stopwordFile = os.path.join('..', 'data', "StopWord.txt")
outputFile = os.path.join('..', 'submit', 'current.csv')

cut_method = jieba.cut_for_search
tokenFile = os.path.join('..', 'tokens', 'search_dict_token.txt')
tokeyFile = os.path.join('..', 'tokens', 'search_dict_tokey.txt')
queryDictFile = os.path.join('..', 'data', 'dict_query.txt')

jieba.load_userdict(queryDictFile)

if __name__ == '__main__':

    stopwords = open(stopwordFile, 'r').read().split()
    queries = open(queryFile, 'r').read().split('\n')
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

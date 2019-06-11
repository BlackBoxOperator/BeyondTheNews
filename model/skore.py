import time, jieba, os, json
import numpy as np
from corpus import initCorpus, makeVector
from pprint import pprint
from tqdm import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stopwordTxt = os.path.join('data', "StopWord.txt")
stopList = open(stopwordTxt,"r").read().split()
title = json.load(open('../DataMining/AllTitle.json'))

if __name__ == '__main__':

    token = open(os.path.join('data', 'token.txt')).read().split('\n')#[:10]
    tokey = open(os.path.join('data', 'tokey.txt')).read().split('\n')#[:10]

    # test for single query and single document
    query = ' '.join([w for w in jieba.cut_for_search("支持陳前總統保外就醫")
                        if w not in stopwordTxt])

    vectorizer = TfidfVectorizer()
    dv = vectorizer.fit_transform(tqdm(token))
    qv = vectorizer.transform([query])
    sims = cosine_similarity(qv, dv)[0]
    ranks = [(title.get(t, t), v) for (v, t) in zip(sims, tokey)]
    ranks.sort(key=lambda e: e[1], reverse=True)
    pprint(ranks)

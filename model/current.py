from tqdm import *
import numpy as np
import time, jieba, os, json, csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from score_functions import twostage
from itertools import starmap

queryFile = os.path.join('..', 'data', 'QS_1.csv')
stopwordFile = os.path.join('..', 'data', "StopWord.txt")
outputFile = os.path.join('..', 'submit', 'current.csv')

cut_method = jieba.cut_for_search
tokenFile = os.path.join('..', 'tokens', 'search_token.txt')
tokeyFile = os.path.join('..', 'tokens', 'search_tokey.txt')



if __name__ == '__main__':

    stopwords = open(stopwordFile, 'r').read().split()
    queries = dict([row for row in csv.reader(open(queryFile, 'r'))][1:])

    trim = lambda f: [t.strip() for t in f if t.strip()]
    token = trim(open(tokenFile).read().split('\n'))[:5000]#[:301]
    tokey = trim(open(tokeyFile).read().split('\n'))[:5000]#[:301]

    if len(token) != len(tokey):
        print('token len sould eq to tokey len')
        exit(0)

    vectorizer = CountVectorizer()
    doc_tf = vectorizer.fit_transform(tqdm(token)).toarray()
    doc_ctx_size = doc_tf.sum(axis=1)
    doc_invert_count = np.where(doc_tf > 0, 1, 0).T.sum(axis=1)
    doc_two_score = np.array(list(starmap(twostage,
                                     zip(doc_tf + 1,
                                         doc_invert_count,
                                         doc_ctx_size))))

    print('\ncorpus vector space - ok\n')

    with open(outputFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['Query_Index'] + ['Rank_{:03d}'.format(i) for i in range(1, 301)]
        writer.writerow(headers)

        for q_id in tqdm(queries):
            query = ' '.join([w for w in cut_method(queries[q_id])
                                if w not in stopwords])
            print('Query: ' + query)
            qry_tf = vectorizer.transform([query]).toarray()
            qry_ctx_size = qry_tf.sum(axis=1)
            qry_invert_count = np.where(qry_tf > 0, 1, 0).T.sum(axis=1)
            qry_two_score = np.array(list(starmap(twostage,
                                     zip(qry_tf + 1,
                                         qry_invert_count,
                                         qry_ctx_size))))

            sims = cosine_similarity(qry_two_score, doc_two_score)[0]
            ranks = [(t, v) for (v, t) in zip(sims, tokey)]
            ranks.sort(key=lambda e: e[-1], reverse=True)
            entry = [q_id] + [e[0] for e in ranks[:300]]
            writer.writerow(entry)

import time, jieba
import numpy as np
from corpus import initCorpus, makeVector
from pprint import pprint
from tqdm import *

def twostage(occurence,collectionFrequency,contextSize,mu=2500,lam=0.8):
    """
    occurence = c(w;d) the number of term w occur in this doc ex: getTextTerm('news_056765')[w]
    collectionFrequency = p(w|C) ex:len(getInvertIndex(w))
    contextSize = len of this doc ex: len(getTextList('news_056765'))
                       [  c(w;d) + \mu * p(w|C)   ]
       ( 1 - \lambda ) [ ------------------------ ] + \lambda * p(w|C)
                       [       |d| + \mu          ]
    """
    dirichlet = (occurence + mu * collectionFrequency)/(contextSize + mu)
    p = (1 - lam) * dirichlet + lam * collectionFrequency
    return np.log10(p)

def TF_IDF_okapi(occurence,tf,idf,avgDocLength,documentLength,k1=1.2,b=0.75):
    """
    occurence = c(w;d) the number of term w occur in this doc
    documentLength = this doc len
    avgDocLength = all data average doc len
                                                      (K1 + 1) * occurrences
    score = termWeight * IDF * ------------------------------------------------------------------
                                occurrences + K1 * ( (1-B) + B * ( documentLength / avgDocLength) )
    """
    numerator = tf * idf * (k1+1) * occurrences
    denominator = occurrences + k1 * ((1-b) +  b * documentLength/avgDocLength)
    return numerator / denominator

# get the inverse document frequency of term
#def getIDF(term,doclen=100000):
#    invI = len(getInvertIndex(term))
#    return np.log10(doclen/invI)

def cosSim(v1,v2):
    return np.dot(v1,v2)/(np.sqrt((v1*v1).sum())*np.sqrt((v2*v2).sum()))

def eucDis(v1,v2):
    return np.sqrt(np.power(v1-v2,2).sum())

def trimKeys(d):
    return {k.strip(): d[k] for k in d}

if __name__ == '__main__':

    Title, TextTerm, TextList, InvertIndex = initCorpus()

    InvertIndex = trimKeys(InvertIndex)

    Terms, VecLen = makeVector(TextTerm)

    """
    Title['news_056765'] -> 阿扁保外就醫 民進黨籲尊重人權 - 政治 - 旺報
    TextTerm['news_056765'] -> {'針對': 1, '法務': 4, '法務部': 4,.......}
    InvertIndex['陳水扁'] -> ['news_067927' 'news_031420' 'news_014034' ...]
    Terms: mapping "term" to idx, or idx back to "term"
    """

    rank = []
    start_time = time.time()

    # test for single query and single document
    jieba.suggest_freq('前總統', True)
    jieba.suggest_freq('就醫', True)
    seg_list = jieba.cut("支持陳前總統保外就醫", cut_all=True)
    query = [w for w in seg_list]


    for docID in tqdm(TextTerm):
        doc = trimKeys(TextTerm[docID])
        #keys = [key for key in doc.keys()]

        twoStageVec = np.zeros(VecLen)
        contextSize = len(TextList[docID])
        for term in doc.keys():
            term = term.strip()
            if term not in Terms: # should fix ""
                if term: print('"{}" not in Terms'.format(term))
            elif term not in InvertIndex:
                print('"{}" not in InvertIndex'.format(term))
            elif term not in doc:
                print('"{}" not in doc'.format(term))
            else:
                twoStageVec[Terms[term]] = twostage(doc[term],
                                                    len(InvertIndex[term]),
                                                    contextSize)

        #twoStageVec = [twostage(doc[key],len(InvertIndex[key]),
        #                len(TextList[docID])) for key in doc.keys()]

        queryVec = np.zeros(VecLen)

        for term in query:
            term = term.strip()
            if term in Terms:
                queryVec[Terms[term]] += 1

        #for i in range(len(query)):
        #    tmpIndex = keys.index(query[i]) if query[i] in keys else -1
        #    if tmpIndex != -1:
        #        queryVec[tmpIndex] += 1


        record = (docID,
                  #cosSim(np.array(twoStageVec),
                  #       np.array(queryVec)),
                  eucDis(np.array(twoStageVec),
                         np.array(queryVec)))

        rank.append(record)

        #print(twoStageVec)
        #print("cos sim:{}".format(record[1]))
        #print("Euclidean distance:{}".format(record[2]))
        #print("--- %s seconds ---" % (time.time() - start_time))

    rank.sort(key=lambda t: t[1], reverse=False)
    pprint(["{}: {}, eucDis = {}".format(
                r[0], Title[r[0]], r[1]) for r in rank[:50]])


    with open("rank.txt", "w") as fo:
        for r in rank[:4000]:
            fo.write("{}: {}, eucDis = {}\n".format(r[0], Title[r[0]], r[1]))

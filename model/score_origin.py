import os, time, sys
import json, jieba
import numpy as np

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

def load_json(jpath):
    with open(jpath, encoding='utf-8') as json_file:
        return json.load(json_file)

DataDir = os.path.join("..", "DataMining")
TitleJson = "AllTitle.json"
TextTermJson = "TextTerm.json"
TextListJson = "TextList.json"
InvertIndexJson = "InvertIndex.json"

if __name__ == '__main__':


    print("loading json... ", end='')
    sys.stdout.flush()
    load = lambda fn: load_json(os.path.join(DataDir, fn))
    jsons = [TitleJson, TextTermJson, TextListJson, InvertIndexJson]
    TitleData, TextTermData, TextListData, InvertIndexData = map(load, jsons)
    print('done')
    """
    TitleData['news_056765'] -> 阿扁保外就醫 民進黨籲尊重人權 - 政治 - 旺報
    TextTermData['news_056765'] -> {'針對': 1, '法務': 4, '法務部': 4,.......}
    InvertIndexData['陳水扁'] -> ['news_067927' 'news_031420' 'news_014034' ...]
    """

    rank = []
    start_time = time.time()

    # test for single query and single document
    jieba.suggest_freq('前總統', True)
    jieba.suggest_freq('就醫', True)
    seg_list = jieba.cut("支持陳前總統保外就醫", cut_all=True)
    query = [w for w in seg_list]


    for docID in TextTermData:
        doc = TextTermData[docID]
        keys = [key for key in doc.keys()]
        twoStageVec = [twostage(doc[key],len(InvertIndexData[key]),
                        len(TextListData[docID])) for key in doc.keys()]

        queryVec = np.zeros(len(twoStageVec))

        for i in range(len(query)):
            tmpIndex = keys.index(query[i]) if query[i] in keys else -1
            if tmpIndex != -1:
                queryVec[tmpIndex] += 1


        record = (docID, cosSim(np.array(twoStageVec),
                                   np.array(queryVec)),
                         eucDis(np.array(twoStageVec),
                                   np.array(queryVec)))
        rank.append(record)

        print(twoStageVec)

        print("cos sim:{}".format(record[1]))
        print("Euclidean distance:{}".format(record[2]))
        print("--- %s seconds ---" % (time.time() - start_time))
        break
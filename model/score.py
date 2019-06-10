import numpy as np
import json
import jieba
import time

def twostage(occurence,collectionFrequency,contextSize,mu=2500,lam=0.8):
    # occurence = c(w;d) the number of term w occur in this doc ex: getTextTerm('news_056765')[w]
    # collectionFrequency = p(w|C) ex:len(getInvertIndex(w))
    # contextSize = len of this doc ex: len(getTextList('news_056765'))
    #                    [  c(w;d) + \mu * p(w|C)   ]
    #    ( 1 - \lambda ) [ ------------------------ ] + \lambda * p(w|C)
    #                    [       |d| + \mu          ]
    dirichlet = (occurence + mu * collectionFrequency)/(contextSize + mu)
    p = (1 - lam) * dirichlet + lam * collectionFrequency
    return np.log10(p)

def TF_IDF_okapi(occurence,tf,idf,avgDocLength,documentLength,k1=1.2,b=0.75):
    # occurence = c(w;d) the number of term w occur in this doc
    # documentLength = this doc len
    # avgDocLength = all data average doc len
    #                                                   (K1 + 1) * occurrences
    # score = termWeight * IDF * ------------------------------------------------------------------
    #                             occurrences + K1 * ( (1-B) + B * ( documentLength / avgDocLength) )
    numerator = tf * idf * (k1+1) * occurrences
    denominator = occurrences + k1 * ((1-b) +  b * documentLength/avgDocLength)
    return numerator / denominator


# get Text Term ex: getTextTerm('news_056765') -> {'針對': 1, '法務': 4, '法務部': 4,.......}
def getTextTerm():
    with open('../Datamining/TextTerm.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


# get invertIndex ex: getInvertIndex('陳水扁') -> ['news_067927' 'news_031420' 'news_014034' ...]
def getInvertIndex():
    with open('../Datamining/InvertIndex.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

# get the inverse document frequency of term
#def getIDF(term,doclen=100000):
#    invI = len(getInvertIndex(term))
#    return np.log10(doclen/invI)

# get the news title ex: getTitle('news_056765') -> 阿扁保外就醫 民進黨籲尊重人權 - 政治 - 旺報
def getTitle():
    with open('../Datamining/AllTitle.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data
# get the doc
def getTextList():
    with open('../Datamining/TextList.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def cosSim(v1,v2):
    return np.dot(v1,v2)/(np.sqrt((v1*v1).sum())*np.sqrt((v2*v2).sum()))
def Euclidean(v1,v2):
    return np.sqrt(np.power(v1-v2,2).sum())


if __name__ == '__main__':
    TextTermData = getTextTerm()
    InvertIndexData = getInvertIndex()
    AllTitleData = getTitle()
    TextListData = getTextList()

    start_time = time.time()

    # test for single query and single document
    jieba.suggest_freq('前總統', True)
    jieba.suggest_freq('就醫', True)
    seg_list = jieba.cut("支持陳前總統保外就醫", cut_all=True)
    query = [w for w in seg_list]


    for docID in TextTermData:
        a = TextTermData[docID]
        keys = [key for key in a.keys()]
        twoStageVec = [twostage(a[key],len(InvertIndexData[key]),len(TextListData['news_056765'])) for key in a.keys()]
        queryVec = np.zeros(len(twoStageVec))

        for i in range(len(query)):
            tmpIndex = keys.index(query[i]) if query[i] in keys else -1
            if tmpIndex != -1:
                queryVec[tmpIndex] += 1

        score1 = cosSim(np.array(twoStageVec),np.array(queryVec))
        score2 = Euclidean(np.array(twoStageVec),np.array(queryVec))
        print(twoStageVec)
        print("cos sim:{}".format(score1))
        print("Euclidean distance:{}".format(score2))
        print("--- %s seconds ---" % (time.time() - start_time))



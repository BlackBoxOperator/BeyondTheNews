import os, json

outputFile = os.path.join('..', 'data', 'InvertIndex.txt')
textTermFile = os.path.join('..', 'data', 'TextTerm.json')

#建立一個新字典，key = term，value = 出現這個term的文章
wordDict = dict()

#讀取已經算好每篇文章的term frequency的json檔
docDict = json.load(open(textTermFile,"r"))

#讀取docDict 的key(新聞ID)，value(字典，包含此篇新聞的tf)

for newsName,termF in docDict.items():
    #下面for做的是讀取每個term，檢查他是否出現在wordDict中，如果沒有，新建這個key
    #然後value = 有出現這個字的文章(是一個set，避免重複出現同樣的文章在裡面)
    for term in termF.keys():
        if wordDict.get(term) == None:
            newsSet = set()
            newsSet.add(newsName)
            wordDict[term] = newsSet
        else:
            wordDict[term].add(newsName)
#最後將每個term 對應的set轉成list(json不存在set的儲存方式)
for term,value in wordDict.items():
    wordDict[term] = list(value)

json.dump(wordDict,open(outputFile,"w"))

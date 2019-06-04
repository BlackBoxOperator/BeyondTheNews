import json;

wordDict = dict()
InFile = open("TextTerm.json","r")
docDict = json.load(InFile)

for newsName,termF in docDict.items():
    for term in termF.keys():
        if wordDict.get(term) == None:
            newsSet = set()
            newsSet.add(newsName)
            wordDict[term] = newsSet
        else:
            wordDict[term].add(newsName)

for term,value in wordDict.items():
    wordDict[term] = list(value)


OutFile = open("InvertIndex.txt","w")
json.dump(wordDict,OutFile)


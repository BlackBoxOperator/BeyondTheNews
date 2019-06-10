import json

File = open("TextList.json")
newsDict = json.load(File)

outputDic = dict()
newName = "news_"
count = 1

for key,value in newsDict.items():
    termdic = dict()
    for term in value:
        if termdic.get(term) == None:
            termdic[term] = 1
        else:
            termdic[term] += 1
    outputDic[newName + "{:06d}".format(count)] = termdic
    count += 1
OutFile = open("TextTerm.json","w")
json.dump(outputDic,OutFile)


import json
"""
這份程式主要在數每篇文章的TF，並且重新製作一個字典，存至 TextList.json
"""

#載入檔案
File = open("TextList.json")
newsDict = json.load(File)

#建立輸出字典 outputDic
outputDic = dict()

#所有文章的共同標題
newName = "news_"
#數現在是第幾篇文章
count = 1

for key,value in newsDict.items():
	#建立一個數文章TF的字典
    termdic = dict()

    #從每一篇文章中數每個出現過的term，存進termdic，
    for term in value:
        if termdic.get(term) == None:
            termdic[term] = 1
        else:
            termdic[term] += 1
    #outputDic 的 key = newsID , value = 一個字典(每個term 他的frequency)
    outputDic[newName + "{:06d}".format(count)] = termdic
    count += 1

#檔案輸出
OutFile = open("TextTerm.json","w")
json.dump(outputDic,OutFile)

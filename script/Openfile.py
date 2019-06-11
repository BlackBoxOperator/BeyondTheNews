import json
import jieba

#"""
#這個檔案負責把原始文章利用jieba，切成一個一個term，
#並建立字典key = newsID, value = Documents term frequency，
#轉存成 "TextList.json";
#"""

data = open("url2content.json","r") #開啟官方給的原始文章
stop = open("StopWord.txt","r") #開啟停用詞的列表

#"""
#stopList 製作停用詞的列表，把所有停用詞加入倒stopList中

#"""
stopList = list()
for line in stop.readlines():
    line = line.strip('\n')
    stopList.append(line)
#print(stopList)


textname = "news_" #每天文章的共同前置標題
text = json.load(data) #把原始文章的字典存入text
#print(type(text))
keylist = list(text.keys()) #儲存 text 的key
#print(type(keylist))

#print(type(text1))
#print(remainderWords)

#""""
#建立空字典 processText，儲存最後的output資料
#"""
processText = dict()
for index in range(100000):
    #以下兩行把每篇新聞的原始文章抽出來，並且用節巴進行全斷詞(所有可能的切法都切 cut_all = True)
    text1 = text[keylist[index]]
    test1 = jieba.cut(text1, cut_all = True)

    #切割完成後，利用stopList，刪除停用詞，並且建成一個list
    remainderWords = list(filter(lambda a: a not in stopList and a != '\n' and a != ' ', test1))
    #建立字典
    processText[textname + "{:06d}".format(index + 1)] = remainderWords

#for key,value in processText.items() and i in range(10):
#    print(key,value)

#輸出檔案
outfile = open("TextList.json","w")
json.dump(processText,outfile)

import os, json, jieba

outputFile = os.path.join('..', 'data', "TextList.json")
url2contentFile = os.path.join('..', 'data', 'url2content.join')
stopwordFile = os.path.join('..', 'data', 'stopword.txt')


"""
這個檔案負責把原始文章利用jieba，切成一個一個term，
並建立字典key = newsID, value = Documents term frequency，
轉存成 "TextList.json";
"""

data = open(url2contentFile,"r") #開啟官方給的原始文章
stop = open(stopwordFile,"r") #開啟停用詞的列表

"""
stopList 製作停用詞的列表，把所有停用詞加入倒stopList中
"""

stopList = list()
for line in stop.readlines():
    line = line.strip('\n')
    stopList.append(line)


textname = "news_" #每天文章的共同前置標題
text = json.load(data) #把原始文章的字典存入text
keylist = list(text.keys()) #儲存 text 的key

""""
建立空字典 processText，儲存最後的output資料
"""
processText = dict()
for index in range(100000):
    """
    以下兩行把每篇新聞的原始文章抽出來，
    並且用 jieba 進行全斷詞(所有可能的切法都切 cut_all = True)
    """
    text1 = text[keylist[index]]
    test1 = jieba.cut(text1, cut_all = True)

    #切割完成後，利用stopList，刪除停用詞，並且建成一個list
    remainderWords = list(filter(lambda a: a not in stopList and a != '\n' and a != ' ', test1))
    #建立字典
    processText[textname + "{:06d}".format(index + 1)] = remainderWords

#輸出檔案
json.dump(processText, open(outputFile,"w"))

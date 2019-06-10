import json
import jieba

data = open("url2content.json","r")
stop = open("StopWord.txt","r")

stopList = list()
for line in stop.readlines():
    line = line.strip('\n')
    stopList.append(line)
#print(stopList)


textname = "news_"
text = json.load(data)
#print(type(text))
keylist = list(text.keys())
#print(type(keylist))

#print(type(text1))
#print(remainderWords)

processText = dict()
for index in range(100000):
    text1 = text[keylist[index]]
    test1 = jieba.cut(text1, cut_all = True)
    remainderWords = list(filter(lambda a: a not in stopList and a != '\n' and a != ' ', test1))
    processText[textname + "{:06d}".format(index)] = remainderWords

outfile = open("TextList.json","w")
json.dump(processText,outfile)

import os, sys, csv, json, re, jieba
from pprint import pprint
from tqdm import *

url2contCSV = os.path.join('..', 'data', "simple_url2content.csv")
stopwordTxt = os.path.join('..', 'data', "simple_stopword.txt")
idx2URLCSV = os.path.join('..', 'data', 'simple_NC_1.csv')
queryDictFile = os.path.join('..', 'data', 'simple_dict.txt')
tokenFile = os.path.join('..', 'tokens', 'simple_search_dict_token.txt')
tokeyFile = os.path.join('..', 'tokens', 'simple_search_dict_tokey.txt')
ignoreFile = os.path.join('..', 'tokens', 'simple_search_dict_ignore.txt')

if input('save token as {}? enter to continue:'.format(tokenFile)).strip(): exit(1)
if input('save tokey as {}? enter to continue:'.format(tokeyFile)).strip(): exit(1)
if input('save ignore as {}? enter to continue:'.format(ignoreFile)).strip(): exit(1)

print("opening file... ", end='')
sys.stdout.flush()
data = open(url2contCSV, "r")
stop = open(stopwordTxt,"r")
csvfile = open(idx2URLCSV, 'r')
print("done")

csvr = csv.reader(csvfile); next(csvr, None)
index2URL = {row[0]: row[1] for row in csvr}

stopList = set(stop.read().split())

print("loading json... ", end='')
sys.stdout.flush()
csvr = csv.reader(data); next(csvr, None)
cont = {row[0]: row[1] for row in csvr}
print("done")

def retain_chinese(line):
    return re.compile(r"[^\u4e00-\u9fa5]").sub('',line)

tokey = open(tokeyFile, "w")
token = open(tokenFile, "w")
ignore = open(ignoreFile, "w")


jieba.load_userdict(queryDictFile)

for index in tqdm(index2URL):

    text = retain_chinese(cont[index2URL[index]]).strip()
    if not text or text.startswith('《苹果》论坛欢迎投稿'):
        ignore.write(index2URL[index] + '\n')
        continue

    tokey.write(index + '\n')
    token.write(' '.join([w for w in jieba.cut_for_search(text)
                            if w.strip() and w not in stopList]) + '\n')

tokey.close()
tokey.close()
ignore.close()

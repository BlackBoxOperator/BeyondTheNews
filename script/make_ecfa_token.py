import os, sys, csv, json, re, jieba
from pprint import pprint
from tqdm import *
"""
這個檔案負責把原始文章利用jieba，切成一個一個term，
並建立字典key = newsID, value = Documents term frequency，
轉存成 "TextList.json";
"""

def strQ2B(ustring):
    """把字串全形轉半形"""
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全形空格直接轉換
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全形字元（除空格）根據關係轉化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

url2contCSV = os.path.join('..', 'data', "url2content.csv")
stopwordTxt = os.path.join('..', 'data', "stopword.txt")
idx2URLCSV = os.path.join('..', 'data', 'NC_1.csv')
tokenFile = os.path.join('..', 'tokens', 'ecfa_token.txt')
tokeyFile = os.path.join('..', 'tokens', 'ecfa_tokey.txt')
ignoreFile = os.path.join('..', 'tokens', 'ecfa_ignore.txt')

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

"""
stopList 製作停用詞的列表，把所有停用詞加到stopList中

"""
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

for index in tqdm(index2URL):

    raw_text = strQ2B(cont[index2URL[index]]).upper()
    text = retain_chinese(raw_text).strip()
    if not text or text.startswith('《蘋果》論壇歡迎投稿'):
        ignore.write(index2URL[index] + '\n')
        continue

    tokey.write(index + '\n')
    token.write(' '.join([w for w in jieba.cut_for_search(text)
                            if w.strip() and w not in stopList]) \
                            + ' '.join(['ECFA'] * raw_text.count('ECFA')) \
                            + '\n')

tokey.close()
tokey.close()
ignore.close()

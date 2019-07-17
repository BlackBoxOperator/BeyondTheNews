import os, sys, csv, json, re, jieba
from pprint import pprint
from tqdm import *

def extract_domain(url):
    url = url[url.index("://") + len("://"):]
    domain = url[:url.index('/') if '/' in url else len(url)]
    return domain

d2n = {
        'www.chinatimes.com': '中時',
        'tw.news.appledaily.com': '蘋果',
        'news.ltn.com.tw': '自由',
        'news.tvbs.com.tw': '聯利',
        'tw.appledaily.com': '蘋果',
        'udn.com': '聯合',
        'tw.sports.appledaily.com': '蘋果',
        'tw.lifestyle.appledaily.com': '蘋果',
        'tw.entertainment.appledaily.com': '蘋果',
        'tw.finance.appledaily.com': '蘋果',
        }

labelCSV = os.path.join('..', 'data', "TD.csv")
urlCSV = os.path.join('..', 'data', 'NC_1.csv')
titleJson = os.path.join('..', 'data', 'title.json')

print("opening file... ", end='')
sys.stdout.flush()
labelfile = open(labelCSV, "r")
urlfile = open(urlCSV, 'r')
titlefile = open(titleJson, 'r')
print("done")

print("loading as dict...", end='')
sys.stdout.flush()
title = json.load(titlefile)
csvr = csv.reader(urlfile); next(csvr, None)
i2u = {row[0]: row[1] for row in csvr}
csvr = csv.reader(labelfile); next(csvr, None)
label = [tuple([r[0], r[2], d2n[extract_domain(i2u[r[1]])], r[1], title[r[1]]]) for r in csvr]
#label = [tuple([r[0], r[2], r[1]]) for r in csvr]
print("done")

with open('NNC.csv', "w", newline='', encoding="UTF-8") as output:
    writer = csv.writer(output)
    writer.writerow(['Query', 'Relevance', 'Domain', 'News_Index', 'Title'])
    #writer.writerow(['Query', 'Relevance', 'News_Index'])
    label.sort(reverse=True)
    for row in label:
        writer.writerow(row)

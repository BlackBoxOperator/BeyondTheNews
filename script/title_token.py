import os, sys, csv, json, jieba, re

titleJson = os.path.join('..', 'data', "title.json")
titles = json.load(open(titleJson, "r"))

cut_method = jieba.cut_for_search
queryDictFile = os.path.join('..', 'data', 'dict_query.txt')
jieba.load_userdict(queryDictFile)

stopwordFile = os.path.join('..', 'data', "StopWord.txt")
stopwords = set(open(stopwordFile, 'r').read().split())

def retain_chinese(line):
    return re.compile(r"[^\u4e00-\u9fa5]").sub('', line).replace('臺', '台')

if len(sys.argv) < 2:
    print('usage: {} csv_file'.format(sys.argv[0]))
    exit(0)
filename = sys.argv[1]
if not os.path.isfile(filename): print(filename, "doesn't exist"), exit(1)

for q, *ids in [q for q in csv.reader(open(filename, 'r'))][1:]:
    print('query: {}'.format(q))
    for news in ids:
        title = retain_chinese(titles.get(news, '')).strip()
        if title and title != "Non":
            title_token = '{}'.format(' '.join([w for w
                in cut_method(title) if w not in stopwords]))
            print(title_token)

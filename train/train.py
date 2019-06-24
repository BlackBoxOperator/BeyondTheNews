from tqdm import *
import numpy as np
import os, datetime, json, re, jieba
from gensim import corpora
from gensim.models import Phrases
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

def retain_chinese(line):
    return re.compile(r"[^\u4e00-\u9fa5]").sub('', line).replace('臺', '台')

class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        if self.epoch == 0:
            self.bar = tqdm(total=model.epochs)

    def on_epoch_end(self, model):
        self.bar.update(1)
        self.epoch += 1
        if self.epoch == model.epochs:
            self.bar.close()
            self.bar = None

titleJson = os.path.join('..', 'data', "title.json")
stopwordFile = os.path.join('..', 'data', "StopWord.txt")
tokenFile = os.path.join('..', 'tokens', 'search_dict_token.txt')
tokeyFile = os.path.join('..', 'tokens', 'search_dict_tokey.txt')

cut_method = jieba.cut_for_search
queryDictFile = os.path.join('..', 'data', 'dict.txt')
jieba.load_userdict(queryDictFile)

trim = lambda f: [t.strip() for t in f if t.strip()]

print("opening file...")

docs = trim(open(tokenFile).read().split('\n'))#[:301]#[:5000]
docIDs = trim(open(tokeyFile).read().split('\n'))#[:301]#[:5000]
stopwords = open(stopwordFile, 'r').read().split()
titles = json.load(open(titleJson, "r"))

print("""
appending title to document...
""")

for i, key in enumerate(tqdm(docIDs)):
    title = retain_chinese(titles.get(key, '')).strip()
    if title and title != "Non":
        title_token = ' {}'.format(' '.join([w for w
            in cut_method(title) if w not in stopwords]))
        docs[i] += title_token

print("spliting tokens...")
docsTokens = [doc.split() for doc in tqdm(docs)]

print("creating model...")
model = Word2Vec(tqdm(docsTokens), min_count=50, size=100, window=5, workers=3, callbacks=[EpochLogger()])

print("training model...")
model.train(tqdm(docsTokens), total_examples=len(docsTokens), epochs=1, callbacks=[EpochLogger()])

print("saving model...")
model.save("./{}.w2v".format(datetime.datetime.now().strftime("%Y_%m%d_%H%M")))

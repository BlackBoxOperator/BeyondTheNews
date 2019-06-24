import os, datetime # , dill
from tqdm import *
import numpy as np
from gensim import corpora
from gensim.models import Phrases
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

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

tokenFile = os.path.join('..', 'tokens', 'search_dict_token.txt')

trim = lambda f: [t.strip() for t in f if t.strip()]

print("opening file...")

docs = trim(open(tokenFile).read().split('\n'))#[:5000]#[:301]

print("spliting tokens...")
docsTokens = [doc.split() for doc in tqdm(docs)]

print("creating model...")
#model = Word2Vec(tqdm(docsTokens), min_count=50, size=100, window=5, workers=3, callbacks=[EpochLogger()])
model = Word2Vec(tqdm(docsTokens), min_count=50, size=1, window=5, callbacks=[EpochLogger()])

#print("training model...")
#model.train(tqdm(docsTokens), total_examples=len(docsTokens), epochs=1, callbacks=[EpochLogger()])

print("saving model...")
#model.save("./{}.w2v".format(datetime.datetime.now().strftime("%Y_%m%d_%H%M")))
#model.save("./fuck.w2v")
model.save("/home/zxc/Class/WSM/BeyondTheNewsOmega/train/word2vec.model")
#model.save("model.w2v")
#with open("{}.w2v".format(datetime.datetime.now().strftime("%Y_%m%d_%H%M")),'wb') as f:
#    dill.dump(model, f)

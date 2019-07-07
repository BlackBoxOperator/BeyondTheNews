from tqdm import *
import numpy as np
import os, datetime, json, re, jieba
from gensim import corpora
from gensim.models import Phrases
from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences
from gensim.models.callbacks import CallbackAny2Vec
from logger import EpochLogger

line_count = 341018

sentences = PathLineSentences("wiki_tokens")

print("creating model...")
model = Word2Vec(tqdm(sentences, total=line_count), min_count=5, size=250, window=5, workers=3, callbacks=[EpochLogger()])

print("training model...")
#model.train(tqdm(sentences), total_examples=len(sentences), epochs=150, callbacks=[EpochLogger()])
model.train(tqdm(sentences, total=line_count), total_examples=model.corpus_count, epochs=100, callbacks=[EpochLogger()])

print("saving model...")
model.save("./wiki_{}.w2v".format(datetime.datetime.now().strftime("%Y%m%d_%H%M")))

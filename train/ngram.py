from gensim.test.utils import datapath
from gensim.models.word2vec import Text8Corpus
from gensim.models.phrases import Phrases, Phraser

sentences = open('test.txt', 'r').read().split()
#sentences = Text8Corpus(datapath('wiki_zh_tw.txt'))
print(sentences)
exit(0)
phrases = Phrases(sentences, min_count=1, threshold=1)  # train model

#phrases[[u'trees', u'graph', u'minors']]  # apply model to sentence
#phrases.add_vocab([["hello", "world"], ["meow"]])  # update model with new sentences

bigram = Phraser(phrases)  # construct faster model (this is only an wrapper)
#print(bigram[phrases])  # apply model to sentence

for sent in bigram[sentences]:  # apply model to text corpus
    print(sent)

import os, datetime
from gensim import corpora
from gensim.models import Phrases
from gensim.models import Word2Vec

tokenFile = os.path.join('..', 'tokens', 'search_dict_token.txt')
docs = trim(open(tokenFile).read().split('\n'))#[:5000]#[:301]

docsTokens = np.array([t.split() for t in token])

dictionary = corpora.Dictionary(docsTokens)

model = Word2Vec(docsTokens, min_count=1)

model.train(docsTokens, total_examples=len(docsTokens), epochs=100)

model.save("{}.w2v".format(datetime.datetime.now().strftime("%Y_%m%d_%H%M")))

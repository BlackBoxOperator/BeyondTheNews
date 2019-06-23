import os, datetime
from gensim import corpora
from gensim.models import Phrases
from gensim.models import Word2Vec

tokenFile = os.path.join('..', 'tokens', 'search_dict_token.txt')
docs = trim(open(tokenFile).read().split('\n'))#[:5000]#[:301]

docTokens = np.array([t.split() for t in token])

dictionary = corpora.Dictionary(docTokens)

bigram_transformer = Phrases(docTokens)
model = Word2Vec(bigram_transformer[docTokens], min_count=1)

model.train(docTokens, total_examples=len(docTokens), epochs=100)

model.save("{}.w2v".format(datetime.datetime.now().strftime("%Y_%m%d_%H%M")))

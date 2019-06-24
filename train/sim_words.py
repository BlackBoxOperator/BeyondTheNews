import sys
from gensim.models import Word2Vec

modelFile = sys.argv[1]
#modelFile = os.path.join("..", "train", "model.w2v")

print("loading model")
model = Word2Vec.load(modelFile)
print("loading model done")
while True:
    model.most_similar(positive=input().split())

import sys
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
            self.bar = None

modelFile = sys.argv[1]
#modelFile = os.path.join("..", "train", "model.w2v")

print("loading model")
model = Word2Vec.load(modelFile)
print("loading model done")
while True:
    print(model.wv.most_similar(positive=input('> ').split(), topn=10))

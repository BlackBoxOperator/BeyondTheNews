import sys, os, json

DataDir = os.path.join("..", "DataMining")
TitleJson = "AllTitle.json"
TextTermJson = "TextTerm.json"
TextListJson = "TextList.json"
InvertIndexJson = "InvertIndex.json"

def load_json(jpath):
    with open(jpath, encoding='utf-8') as json_file:
        return json.load(json_file)

def initCorpus():
    global Title, TextTerm, TextList, InvertIndex
    print("loading json... ", end='')
    sys.stdout.flush()
    load = lambda fn: load_json(os.path.join(DataDir, fn))
    jsons = [TitleJson, TextTermJson, TextListJson, InvertIndexJson]
    Title, TextTerm, TextList, InvertIndex = map(load, jsons)
    print('done')
    return Title, TextTerm, TextList, InvertIndex

def makeVector(TextTerm):
    terms = set()
    Terms = {}

    for news in TextTerm:
        terms.update([k.strip() for k in TextTerm[news].keys() if k.strip()])

    for idx, term in enumerate(terms):
        Terms[idx] = term
        Terms[term] = idx

    return Terms, idx + 1

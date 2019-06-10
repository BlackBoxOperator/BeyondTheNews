import os, sys
from corpus import load_json, DataDir, TextTermJson

if __name__ == '__main__':
    print("loading json... ", end=''); sys.stdout.flush()
    TextTerm = load_json(os.path.join(DataDir, TextTermJson))
    print('done')
    terms = set()
    for news in TextTerm:
        terms.update(TextTerm[news].keys())
    with open("terms.txt", "w") as fo:
        for term in terms:
            if not term:
                print("not term")
            #elif term.strip() != term:
            #    print("not strip: '{}'".format(term))
            else:
                fo.write(term.strip() + '\n')


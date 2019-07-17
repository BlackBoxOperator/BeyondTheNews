import os, sys, csv, json

titleJson = os.path.join('..', 'data', "title.json")
titles = json.load(open(titleJson, "r"))
cr = csv.reader(open(os.path.join('..', 'data', 'QS_1.csv'), 'r')); next(cr)
qname = {r[0]: r[1] for r in cr}

if len(sys.argv) < 2:
    print('usage: {} csv_file'.format(sys.argv[0]))
    exit(0)
filename = sys.argv[1]
if not os.path.isfile(filename): print(filename, "doesn't exist"), exit(1)

for q, *ids in [q for q in csv.reader(open(filename, 'r'))][1:]:
    print('query: {}, {}'.format(q, qname[q]))
    for news in ids:
        print(titles[news])

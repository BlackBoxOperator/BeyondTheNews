import os, json, csv, sys

NCFile = os.path.join('..', 'data', 'NC_1.csv')
url2contentFile = os.path.join('..', 'data', 'url2content.json')

index2URL = {}
with open(NCFile, newline='') as csvfile:
  for row in csv.reader(csvfile):
    index2URL[row[0]] = row[1]

print("loading json... ", end='')
sys.stdout.flush()
with open(url2contentFile, 'r') as f:
    data = json.load(f)
    print('done')
    while True:
        print(data.get(index2URL[input('input index > ')], None))

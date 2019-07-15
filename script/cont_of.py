import os, json, csv, sys

NCFile = os.path.join('..', 'data', 'NC_1.csv')
url2contCSV = os.path.join('..', 'data', "url2content.csv")

index2URL = {}
with open(NCFile, newline='') as csvfile:
  for row in csv.reader(csvfile):
    index2URL[row[0]] = row[1]

print("loading json... ", end='')
sys.stdout.flush()
with open(url2contCSV, 'r') as f:
    csvr = csv.reader(data); next(csvr, None)
    cont = {row[0]: row[1] for row in csvr}
    print('done')
    while True:
        print(data.get(index2URL[input('input index > ')], None))

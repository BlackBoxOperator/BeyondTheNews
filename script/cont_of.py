import json, csv, sys

index2URL = {}
with open('data/NC_1.csv', newline='') as csvfile:
  for row in csv.reader(csvfile):
    index2URL[row[0]] = row[1]

print("loading json... ", end='')
sys.stdout.flush()
with open('data/url2content.json', 'r') as f:
    data = json.load(f)
    print('done')
    while True:
        print(data.get(index2URL[input('input index > ')], None))

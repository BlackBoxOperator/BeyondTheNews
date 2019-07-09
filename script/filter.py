import csv, os, sys
from tqdm import tqdm

"""
remove news in ${1}.csv file from ${2}.csv
"""

reindices = set(open(sys.argv[1], 'r').read().split())

ctx = open(sys.argv[2], 'r')
csvr = csv.reader(ctx); next(csvr, None)

NC = [r for r in csvr if r[0] not in reindices]

with open('output.csv', 'w', newline='', encoding="UTF-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(['index', 'title', 'content'])

    for row in tqdm(NC, ascii = True):

        writer.writerow(row)

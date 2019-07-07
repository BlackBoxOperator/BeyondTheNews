import os, csv

# prove nc1 include in nc2

nc1 = os.path.join('..', 'data', 'NC_1.csv')
nc2 = os.path.join('..', 'data', 'NC_2.csv')

csvr = csv.reader(open(nc1, 'r')); next(csvr, None)
nc1 = {row[0]: row[1] for row in csvr}

csvr = csv.reader(open(nc2, 'r')); next(csvr, None)
nc2 = {row[0]: row[1] for row in csvr}

url1 = set(nc1.values())
url2 = set(nc2.values())
url1.difference(url2)

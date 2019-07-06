import os, csv
from itertools import takewhile

#summary = {}
summary = []
template = []
example = []

def extract_domain(url):
    url = url[url.index("://") + len("://"):]
    domain = url[:url.index('/') if '/' in url else len(url)]
    return domain

domains = set()
print('Invalid URLs:')
ctx = open(os.path.join('..', 'data', 'NC_2.csv'), 'r')
csvr = csv.reader(ctx); next(csvr, None)
nc = {row[0]: row[1] for row in csvr}

for iden in nc:
    if "://" in nc[iden]:
        domain = extract_domain(nc[iden])
        domains.add(domain)
        #summary.setdefault(domain, set()).add(nc[iden])
        summary.append(nc[iden])
        if not any([nc[iden].startswith(ptn) for ptn in template]):
            template.append(''.join(takewhile(lambda x:not x.isdigit(), nc[iden])))
            example.append(nc[iden])

    elif nc[iden]:
        print(nc[iden])

print('=' * 30)

print("Domains:")
for t in template:
    print(t)
print()
print("URLs:")
for ex in example:
    print(ex)

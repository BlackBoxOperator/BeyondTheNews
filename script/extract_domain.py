def extract_domain(url):
    url = line[line.index("://") + len("://"):]
    domain = url[:url.index('/') if '/' in url else len(url)]
    return domain

domains = set()
print('Invalid URLs:')
ctx = open('data/NC_1.csv', 'r').read()
for line in ctx.split('\n'):
    if "://" in line:
        domain = extract_domain(line)
        domains.add(domain)
    elif line:
        print(line)

print('=' * 30)

print("Domains:")
for domain in domains:
    print(domain)

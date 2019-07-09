import json, csv, sys, os

"""
convert url2content.json to csv
"""

log = print

def check_file(name):
    if not os.path.isfile(name):
        print("no file named {}".format(name)), exit(0)
    return name

def writerow(writer, row, log):
    try:
        writer.writerow(row)
    except UnicodeEncodeError:
        index, _, _ = row
        log(index, "- Encode Error -")
        writer.writerow([handle_uee(r) for r in row])

if len(sys.argv) < 3:
    print("usage: {} in.json out.csv".format(sys.argv[0])), exit(0)

data = open(check_file(sys.argv[1]), "r")
cont = json.load(data)

writer = csv.writer(open(sys.argv[2], 'w'))
writerow(writer, ['url', 'content'], log)

for url in cont:
    writerow(writer, [url, cont[url]], log)


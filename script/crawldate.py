import webbrowser, re, csv, os, sys
import requests as rq
from bs4 import BeautifulSoup
from tqdm import tqdm

resc = lambda s: s.replace("\r", '').replace("", "").replace("\n", "")

nonsense = ['(中時電子報)',
            '想看更多新聞嗎',
            '＞＞＞更多新聞請點此＜']
nonwords = ['小', '中', '大']

paynews = ['tw.finance.appledaily.com',
           'tw.appledaily.com',
           'tw.entertainment.appledaily.com',
           'tw.sports.appledaily.com',
           'tw.lifestyle.appledaily.com',
           'tw.news.appledaily.com',
           'tw.news.appledaily.com']

def rm_tag(s):
    return re.sub('<[^>]*>', '', s)

def download(url):
    downcount = 0
    while True:
        try:
            request = rq.get(url, timeout = 10)
            if request.status_code != 200:
                return None, "- status: {} -".format(request.status_code)
        except rq.exceptions.Timeout:
            downcount += 1
            if downcount > 5:
                return None, "- timeout too many times -"
            continue
        except Exception as e:
            return None, "- exception: {} -".format(e)

        return request.text, None


def rename_dialog(ques, alert, default):
    print()
    name = input(ques + '?\n(enter to cont, input to rename):').strip()
    if name:
        print()
        yn = input(alert.format(name) + '?\n(enter to cont, input to break):').strip()
        if yn:
            print("terminated")
            exit(0)
        return name
    else:
        return default

def handle_uee(filename):
    return repr(filename)[1:-1]

def writerow(writer, row, log):
    try:
        writer.writerow(row)
    except UnicodeEncodeError:
        index, _, _ = row
        log(index, "- Encode Error -")
        writer.writerow([handle_uee(r) for r in row])

def domain_attr_of(url, attrs):
    for domain in attrs:
        if domain in url:
            return attrs[domain]
    print("cannot find domain pattern in", url)
    webbrowser.open(url), exit(0)

def get_date(idx, url, soup, log):
    attrs = {
            'www.chinatimes.com': \
                    lambda s:s.find('time')['datetime'],
            'udn.com': \
                    lambda s:s.find('meta', attrs={'name': 'date'})['content'],
            'news.ltn.com.tw': \
                    lambda s:s.find('span', attrs={'class': 'viewtime'}).get_text(),
            'appledaily.com': \
                    lambda s:s.find('div', attrs={'class': 'ndArticle_creat'}).get_text(),
            'news.tvbs.com.tw':
            lambda s:s.find('div', attrs={'class': 'icon_time time leftBox2'}).get_text(),
            'home.appledaily.com.tw': \
                    lambda s:s.find('span', attrs={'class': 'date'}).get_text(),
            }
    try:
        return domain_attr_of(url, attrs)(soup)
    except Exception as e:
        if 'ltn.com.tw' in url:
            try:
                return soup.find('div', attrs={'class': 'date'}).get_text()
            except Exception as e:
                log(idx, url, "- {} -".format(e))
                return 'none'
        else:
            log(idx, url, "- {} -".format(e))
            return 'none'

ctx = open(os.path.join('..', 'data', 'NC_2.csv'), 'r')
csvr = csv.reader(ctx); next(csvr, None)

NC = list(csvr)

start = 0
end = len(NC)

if len(sys.argv) > 1:
    start = int(sys.argv[1])

if len(sys.argv) > 2:
    end = int(sys.argv[2])

NC = NC[start:end]

print("start from: {} to {}".format(NC[0][0], NC[-1][0]))

if input("Enter to continue else break:"):
    print("terminated"), exit(0)

log_loc = os.path.join('..', 'data', 'log.txt')
cont_loc = os.path.join('..', 'data', 'content.csv')

log_loc = rename_dialog("save log to: {}".format(log_loc),
                        "relocate log file to {}",
                        log_loc)

cont_loc = rename_dialog("save content to: {}".format(cont_loc),
                         "relocate content file to {}",
                         cont_loc)

mode = 'a' if start else 'w'

print("start crawling...")

with open(log_loc, mode, encoding="UTF-8") as logfile:
    log = lambda *ss: logfile.write(' '.join([str(s) for s in ss]) + '\n')

    with open(cont_loc, mode, newline='', encoding="UTF-8") as csvfile:

        writer = csv.writer(csvfile)

        if not start: writerow(writer, ['index', 'date'], log)

        for index, url in tqdm(NC, ascii = True):

            html, errmsg = download(url)
            if errmsg:
                log(index, errmsg, url)
                writerow(writer, [index, '', ''], log)
                continue

            soup = BeautifulSoup(html, "html.parser")
            date = ''.join([c for c in get_date(index, url, soup, log) if c in '0123456789/-: noe']).strip()
            if not date: print('cannot get date of', index), exit(0)
            #author = get_author(url, soup)
            #if not author: print('cannot get author of', index), exit(0)
            writerow(writer, [index, date], log)

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

article_attrs = {
        'www.chinatimes.com': {'class': 'article-body'},
        'udn.com': {'id': 'story_body_content'},
        'news.ltn.com.tw': {'class': 'whitecon articlebody'},
        'news.tvbs.com.tw': {'id':'news_detail_div'},
                            #{'class': 'newsdetail_content'},
        'home.appledaily.com.tw': {'class': 'ncbox_cont'},
        }

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

def article_attrs_by(url):
    for domain in article_attrs:
        if domain in url:
            return article_attrs[domain]
    print("cannot find domain pattern in", url)
    webbrowser.open(url), exit(0)

ctx = open(os.path.join('..', 'data', 'NC_2.csv'), 'r')
csvr = csv.reader(ctx); next(csvr, None)

NC = list(csvr)

start = 0
end = len(csvr)

if len(sys.argv) > 1:
    start = int(sys.argv[1])

if len(sys.argv) > 2:
    end = int(sys.argv[2])

NC = csvr[start:end]

print("start from:", NC[0][0])
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

        if not start: writerow(writer, ['index', 'title', 'content'], log)

        for index, url in tqdm(NC, ascii=True):

            try:
                request = rq.get(url)
                html = request.text
                if request.status_code != 200:
                    log(index, "- status: {} -".format(request.status_code), url)
            except Exception as e:
                log(index, "- invalid URL -", e, url, e)
                writerow(writer, [index, '', ''], log)
                continue

            soup = BeautifulSoup(html, "html.parser")
            title = resc(soup.title.get_text() if soup.title else '')

            #if not title:
            #    log(index, "- no title (404) -", url)

            if any(pay in url for pay in paynews):
                log(index, "- skip apple -", url)
                writerow(writer, [index, title, ''], log)
                continue

            article = soup.find("div", attrs=article_attrs_by(url))

            if not article:
                """
                404 not found
                """
                log(index, '- no article (404) -', url)
                writerow(writer, [index, title, ''], log)
                continue

            paragraphs = article.findChildren("p")

            if not paragraphs or ('tvbs' in url and len(paragraphs) < 5):
                content = resc(''.join([s for s in article.get_text().split() \
                                    if not any([s.startswith(n) for n in nonsense])
                                    and not any([s == n for n in nonwords])]))
                writerow(writer, [index, title, content], log)
            else:
                paragraphs += article.find_all(re.compile('^h[1-6]$'))
                content = resc(''.join([s for s in [p.get_text().strip() for p in paragraphs] \
                                            if not any([s.startswith(n) for n in nonsense])
                                            and not any([s == n for n in nonwords])]))
                writerow(writer, [index, title, content], log)

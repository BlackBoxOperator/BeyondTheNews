import webbrowser, re, csv, os
import requests as rq
from bs4 import BeautifulSoup
from tqdm import tqdm

resc = lambda s: s.replace("\r", '').replace("", "").replace("\n", "")

f = open(os.path.join('..', 'data', 'error_log.txt'), 'w', encoding="UTF-8")
print = lambda *ss: f.write(' '.join([str(s) for s in ss]) + '\n')

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

def article_attrs_by(url):
    for domain in article_attrs:
        if domain in url:
            return article_attrs[domain]
    print("cannot find domain pattern in", url)
    webbrowser.open(url), exit(0)

ctx = open(os.path.join('..', 'data', 'NC_2.csv'), 'r')
csvr = csv.reader(ctx); next(csvr, None)


# assign range here, 80w
# NC = list(csvr)[400000:] # from 40w to 80w
NC = list(csvr)

with open(os.path.join('..', 'data', 'content.csv'), 'w', newline='', encoding="UTF-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['index', 'title', 'content'])

    for index, url in tqdm(NC, ascii=True):

        try:
            request = rq.get(url)
            html = request.text
            if request.status_code != 200:
                print(index, "- status: {} -".format(request.status_code), url)
                writer.writerow([index, '', ''])
        except Exception as e:
            print(index, "- invalid URL -", e, url, e)
            writer.writerow([index, '', ''])
            continue

        soup = BeautifulSoup(html, "html.parser") 
        title = resc(soup.title.get_text() if soup.title else '')

        #if not title:
        #    print(index, "- no title (404) -", url)
            
        if any(pay in url for pay in paynews):
            print(index, "- skip apple -", url)
            writer.writerow([index, title, ''])
            continue

        article = soup.find("div", attrs=article_attrs_by(url))

        if not article:
            """
            404 not found
            """
            print(index, '- no article (404) -', url)
            writer.writerow([index, title, ''])
            continue

        paragraphs = article.findChildren("p")

        if not paragraphs or ('tvbs' in url and len(paragraphs) < 5):
            content = resc(''.join([s for s in article.get_text().split() \
                                if not any([s.startswith(n) for n in nonsense])
                                and not any([s == n for n in nonwords])]))
            writer.writerow([index, title, content])
        else:
            paragraphs += article.find_all(re.compile('^h[1-6]$'))
            content = resc(''.join([s for s in [p.get_text().strip() for p in paragraphs] \
                                        if not any([s.startswith(n) for n in nonsense])
                                        and not any([s == n for n in nonwords])]))
            writer.writerow([index, title, content])

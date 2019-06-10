import json

with open('data/url2content.json', 'r') as f:
    data = json.load(f)
    # non-existing news
    print(data['/appledaily/article/adcontent/20170114/37518814/'])
    print(data['/appledaily/article/adcontent/20170817/37750863/'])
    print(data['/appledaily/article/adcontent/20161223/37494145/'])
    print(data['/appledaily/article/adcontent/20161101/37432052/'])
    print(data['/appledaily/article/adcontent/20170414/37616791/'])
    print(data['/appledaily/article/adcontent/20170729/37730727/'])
    print(data['/appledaily/article/adcontent/20161021/37424082/'])
    print(data['/appledaily/article/adcontent/20170803/37736089/'])
    print(data['/appledaily/article/adcontent/20170721/37722716/'])
    print(data['/appledaily/article/adcontent/20171208/37868026/'])
    print(data['/appledaily/article/adcontent/20170526/37662239/'])
    print(data['/appledaily/article/adcontent/20170715/37715548/'])


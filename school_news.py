import requests
from bs4 import BeautifulSoup
import logging
import time
from fake_useragent import UserAgent
from base64 import b64encode
from urllib.parse import quote
import re

ua = UserAgent(verify_ssl=False)
# 生成USER-ANGENT

news_type = {
    'xy': '/news/syyw/?page=',
    'jw': 'http://jwc.gdst.cc/jiaowuchu/index.aspx?lanmuid=94&sublanmuid=677&page=',
}


def get_news(origin, page=1):
    # 获取新闻列表,接受前端的请求的来源（院别）,页数默认为1，新闻获取数量为15条
    if origin != 'jw':
        url = 'http://www.gdust.cn/' + news_type[origin] + str(page)
    else :
        url = news_type[origin] + str(page)
    try:
        news_list = []
        headers = {'user-agent': ua.chrome}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find(class_='article').find_all('li')
    except Exception as e:
            logging.warning(u'学院官网连接超时错误:%s' % e)
            return {}
    else:
        '''
        news_page = soup.find(class_='pageinfo').getText
        news_page = re.search("页次：(\d{1,2})\/",str(news_page))[1]
        if page == news_page:

        '''
        for row in rows:
            date = row.find(class_='date')
            # 匹配时间
            date = date.getText()
            date.replace('/', '-')
            title = row.a.string
            url = row.a.attrs['href']
            url = quote(url)
            if origin == 'jw':
                data = {
                    'title': title,
                    'url':  url,
                    'time': date,
                    'type': origin
                }
            else:
                data = {
                    'title': title,
                    'url': u'http://www.gdst.cc/' + url,
                    'time': date,
                    'type': origin
                }

            news_list.append(data)
        '''
        #else:
            #return{}

        '''
    return news_list


def get_news_detail(url):
    # 获取新闻详细
    try:
        headers = {'user-agent': ua.chrome}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
        rows = soup.find(class_='articleinfor')
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        content = ""
        title = ''
        date = ''
        if rows:
            title = rows.find(class_="title").string
            date = rows.find(class_="info")
            date = re.search('\d.*\d',str(date))[0]
            content = rows.find(class_="content")
            content = str(content).replace("src=\"/", "src=\"http://www.gdust.cn/")
            content = b64encode(content.encode())
    return {
        'title': title,
        'time': date,
        'html': bytes.decode(content),
    }

def get_notice_detail(url):
     # 获取教务处详细
    try:
        headers = {'user-agent': ua.chrome}
        r = requests.get(url+'?lanmuid=94&sublanmuid=677', headers=headers)
        soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
        rows = soup.find(class_='article')
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        content = ""
        title = ""
        date = ""
        if rows:
            title = rows.find(class_="title").find_all('h1')
            date = rows.find(class_="info")
            date = re.search('\d.*\d',str(date))[0]
            content = rows.find(class_="content")
            content = str(content).replace("src=\"/", "src=\"http://www.gdust.cn/")
            content = b64encode(content.encode())
    return {
        'title': title,
        'time': date,
        'html': bytes.decode(content),
    }







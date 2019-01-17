import requests
from bs4 import BeautifulSoup
import logging
from .new_cache import new_cache
from fake_useragent import UserAgent
from base64 import b64encode
from urllib.parse import quote
import re
from app import redis_store
import ast
import config


@new_cache('list')
def get_news(origin, faculty, page=1):
    # 获取新闻列表,接受前端的请求的来源（院别）,页数默认为1，新闻获取数量为15条
    if origin == 'xy':
        url = 'http://www.gdust.cn/' + \
            config.NEWS_TYPE[origin] + str(page)
    elif origin == 'xb':
        url = 'http://www.gdust.cn/' + \
            config.NEWS_TYPE[faculty] + str(page)
    else:
        url = config.NEWS_TYPE[origin] + str(page)

    try:
        news_list = []
        r = requests.get(url)
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
                    'url': url,
                    'time': date,
                    'type': origin
                }
            else:
                data = {
                    'title': title,
                    'url': u'http://www.gdst.cc' + url,
                    'time': date,
                    'type': origin
                }

            news_list.append(data)

    return news_list


@new_cache('detail')
def get_news_detail(url):
    # 获取新闻详细
    try:
        r = requests.get(url)
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
            date = re.search('\d.*\d', str(date))[0]
            content = rows.find(class_="content")
            content = str(content).replace(
                'src="/', 'src="http://www.gdust.cn/')
            content = b64encode(content.encode())

    return {
        'title': title,
        'time': date,
        'html': bytes.decode(content),
    }


@new_cache('detail')
def get_notice_detail(url):
     # 获取教务处详细
    try:
        r = requests.get(url)
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
            date = re.search('\d.*\d', str(date))[0]
            content = rows.find(class_="content")
            content = str(content).replace(
                'src="/', 'src="http://www.gdust.cn/')
            content = b64encode(content.encode())
    return {
        'title': title,
        'time': date,
        'html': bytes.decode(content),
    }


def get_headline(faculty, page=1):
    news_list = []
    for name in config.ORIGIN_TYPE:
        if name != 'xb':
            key = str(page)
        else:
            key = faculty + '_' + str(page)

        data = ast.literal_eval(bytes.decode(redis_store.hget(name, key)))
        for content in data:
            news_list.append(content)

    news_list.sort(key=lambda element: element['time'], reverse=True)

    return news_list

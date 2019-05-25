import requests
from bs4 import BeautifulSoup
import logging
from .new_cache import new_cache
from base64 import b64encode
from urllib.parse import quote
import re
from app import redis_store
import ast
import config
from app.school_news.services import xm_news as xm


@new_cache('list')
def get_news(origin, faculty, page=1, force_reload=False):
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
        r = requests.get(url, timeout=10)
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}

    else:
        r.encoding = 'uft-8'
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find(class_='article').find_all('li')
        '''
        news_page = soup.find(class_='pageinfo').getText
        news_page = re.search("页次：(\d{1,2})\/",str(news_page))[1]
        if page == news_page:
        '''
        news_list = []
        for row in rows:
            date = row.find(class_='date')
            # 匹配时间
            date = date.getText()
            date.replace('/', '-')
            title = row.a.string
            url = row.a.attrs['href']
            if url == '#':
                continue
            elif origin == 'jw':
                url = quote(url)
                data = {
                    'title': title,
                    'url': url,
                    'time': date,
                    'type': origin
                }

                news_list.append(data)
            else:
                url = quote(url)
                data = {
                    'title': title,
                    'url': u'http://www.gdust.cn' + url,
                    'time': date,
                    'type': origin
                }

                news_list.append(data)

        return news_list


@new_cache('detail')
def get_news_detail(url, force_reload=False):
    # 获取新闻详细
    try:
        r = requests.get(url, timeout=10)
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
        rows = soup.find(class_='articleinfor')
        if rows:
            try:
                title = rows.find(class_="title").string
                if title is None:
                    title = rows.find(class_="title").find('h1').string
            except BaseException:
                suffix = re.search('(\d{4})\.html', url).group(1)
                url = 'http://www.gdust.cn/index.aspx?lanmuid=63&sublanmuid=671&id=%s' % suffix
                get_news_detail(url)

            else:
                date = rows.find(class_="info")
                date = re.search('\d.*\d', str(date)).group(0)
                content = rows.find(class_="content")
                content = str(content).replace(
                    'src="/', 'src="http://www.gdust.cn/')
                content = b64encode(content.encode())
                html = bytes.decode(content)

                return {
                    'title': title,
                    'time': date,
                    'html': html,
                }


@new_cache('detail')
def get_notice_detail(url, force_reload=False):
     # 获取教务处详细
    try:
        r = requests.get(url, timeout=10)
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
        rows = soup.find(class_='articleinfor')
        title = rows.find(class_="title").h1.string
        date = rows.find(class_="info")
        date = re.search('\d.*\d', str(date)).group(0)
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

        data = redis_store.hget(name, key)
        if data:
            data = ast.literal_eval(bytes.decode(data))
            for content in data:
                news_list.append(content)

    news_list.sort(key=lambda element: element['time'], reverse=True)
    xm_news = xm.get_list()
    if xm_news:
        xm_news.reverse()
        for data in xm_news:
            if data:
                news_list.insert(0, data)
    return news_list

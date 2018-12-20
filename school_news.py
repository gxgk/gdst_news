import requests
from bs4 import BeautifulSoup
import logging
import time
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
# 生成USER-ANGENT

news_type = {
    'xy': '/news/syyw/?page=',
    'jsjx': '/jsjx/xbxw/xbdt/?page=',
    'cjx': '/cjx/xbxw/xbdt/?page=',
    'ysx': '/ysx/xbxw/xbdt/?page=',
    'yyx': '/yyx/xbxw/xbdt/?page=',
    'glx': '/glx/xbxw/xbdt/?page=',
    'jdx': '/jdx/xbxw/xbdt/?page=',
}
notice_tyoe = {
    'xy': '/news/tzgg/',
    'jsjx': '/jsjx/xbxw/tzgg/?page=',
    'cjx': '/cjx/xbxw/tzgg/?page=',
    'ysx': '/ysx/xbxw/tzgg/?page=',
    'yyx': '/yyx/xbxw/tzgg/?page=',
    'glx': '/glx/xbxw/tzgg/?page=',
    'jdx': '/jdx/xbxw/tzgg/?page=',
}

news_list = []
notice_list = []


def get_news(origin, page=1):
    # 获取新闻列表,接受前端的请求的来源（院别）,页数默认为1，新闻获取数量为15条
    url = 'http://www.gdust.cn/' + news_type[origin] + str(page)
    try:
        headers = {'user-agent': ua.chrome}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find(class_='article').find_all('li')
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        for row in rows:
            date = row.find(class_='date')
            # 匹配时间
            date = date.getText()
            date.replace('/', '-')
            title = row.a.string
            url = row.a.attrs['href']
            data = {
                'title': title,
                'url': u'http://www.gdst.cc/' + url,
                'date': date,
                'origin': origin,
            }
            news_list.append(data)

    return news_list


def get_notice(origin, page=1):
    # 获取通告列表，接受前端的请求的来源（院别）,页数默认为1，新闻获取数量为15条
    url = 'http://www.gdust.cn/' + notice_list[origin] + str(page)
    try:
        headers = {'user-agent': ua.chrome}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find(class_='article').find_all('li')
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        for row in rows:
            date = row.find(class_='date')
            # 匹配时间
            date = date.getText()
            date.replace('/', '-')
            title = row.a.string
            url = row.a.attrs['href']
            data = {
                'title': title,
                'url': u'http://www.gdst.cc/' + url,
                'date': date,
                'origin': origin,
            }
            notice_list.append(data)

    return notice_list


def get_news_detail(url):
    # 获取新闻详细
    try:
        headers = {'user-agent': ua.chrome}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find(class_='articleinfor')
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        data = rows

    return rows


def get_notice_detail(url):
    # 获取通告详细
    try:
        headers = {'user-agent': ua.chrome}
        r = requests.get(content['url'], headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find(class_='articleinfor')
    except Exception as e:
        logging.warning(u'学院官网连接超时错误:%s' % e)
        return {}
    else:
        data = rows
    return rows




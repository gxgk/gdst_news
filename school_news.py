import requests
from bs4 import BeautifulSoup
import logging


def get_news():
    news_url = []
    news_list = []
    news_type = {
        'xy': '/news/syyw/',
        'jsjx': '/jsjx/xbxw/xbdt/',
        'cjx': '/cjx/xbxw/xbdt/',
        'ysx': '/ysx/xbxw/xbdt/',
        'yyx': '/yyx/xbxw/xbdt/',
        'glx': '/glx/xbxw/xbdt/',
        'jdx': '/jdx/xbxw/xbdt/',
    }

    for key in news_type:
        # 构建URL
        if key == 'xy':
            # 学院爬取3页，系爬取2页
            for n in range(1, 4):
                url = 'http://www.gdst.cc' + news_type[key] + '?page=' + str(n)
                data = {
                    'url': url,
                    'type': key,
                }
                news_url.append(data)

        else:
            for n in range(1, 3):
                url = 'http://www.gdst.cc' + news_type[key] + '?page=' + str(n)
                data = {
                    'url': url,
                    'type': key,
                }
                news_url.append(data)

    for content in news_url:
        try:
            r = requests.get(content['url'])
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
                    'origin': content['type'],
                }
                news_list.append(data)

    return news_list


def get_notice():
    notice_url = []
    notice_list = []
    notice_type = {
        'xy': '/news/tzgg/',
        'jsjx': '/jsjx/xbxw/tzgg/',
        'cjx': '/cjx/xbxw/tzgg/',
        'ysx': '/ysx/xbxw/tzgg/',
        'yyx': '/yyx/xbxw/tzgg/',
        'glx': '/glx/xbxw/tzgg/',
        'jdx': '/jdx/xbxw/tzgg/',
    }

    for key in notice_type:
        # 构建URL
        if key == 'xy':
            # 学院爬取3页，系爬取2页
            for n in range(1, 4):
                url = 'http://www.gdst.cc' + \
                    notice_type[key] + '?page=' + str(n)
                data = {
                    'url': url,
                    'type': key,
                }
                notice_url.append(data)

        else:
            for n in range(1, 3):
                url = 'http://www.gdst.cc' + \
                    notice_type[key] + '?page=' + str(n)
                data = {
                    'url': url,
                    'type': key,
                }
                notice_url.append(data)

    for content in notice_url:
        try:
            r = requests.get(content['url'])
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
                    'origin': content['type'],
                }
                notice_list.append(data)

    return notice_list


def get_news_detail(news_list):
    news_detail = []
    for content in news_list:
        try:
            r = requests.get(content['url'])
            soup = BeautifulSoup(r.text, 'html.parser')
            rows = soup.find(class_='articleinfor')
        except Exception as e:
            logging.warning(u'学院官网连接超时错误:%s' % e)
            return {}
        else:
            data = {
                'title': content['title'],
                'origin': content['origin'],
                'html': rows,
                'type': 'news',
            }
            news_detail.append(data)

    return news_detail


def get_notice_detail(notice_list):
    notice_detail = []
    for content in notice_list:
        try:
            r = requests.get(content['url'])
            soup = BeautifulSoup(r.text, 'html.parser')
            rows = soup.find(class_='articleinfor')
        except Exception as e:
            logging.warning(u'学院官网连接超时错误:%s' % e)
            return {}
        else:
            data = {
                'title': content['title'],
                'origin': content['origin'],
                'html': rows,
                'type': 'notice'
            }
            notice_detail.append(data)

    return notice_detail

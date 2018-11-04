import requests
from bs4 import BeautifulSoup
import re
import logging


class Base():
    # 爬虫基类
    def __init__(self):
        self.option = {
            'xy': 'news',
            'jsjx': 'jsjx',
            'cjx': 'cjx',
            'ysx': 'ysx',
            'yyx': 'yyx',
            'glx': 'glx',
            'jdx': 'jdx',
        }
        self.news_detail_list = []
        self.notice_detail_list = []

    def set_url(self):
        # 爬取新闻，通知列表
        news_list = []
        notice_list = []
        for key in self.option:
            if key == 'xy':
                for x in range(1, 4):
                    # 学院爬取三页
                    news_url = u'http://www.gdst.cc/news/syyw/?page=' + str(x)
                    # 新闻
                    notice_url = u'http://www.gdst.cc/news/tzgg/?page=' + \
                        str(x)
                    # 通知通告
                    data_1 = {
                        # 存储新闻URL
                        'origin': 'xy',
                        'url': news_url,
                    }
                    data_2 = {
                        # 存储通告URL
                        'origin': 'xy',
                        'url': notice_url,
                    }
                    news_list.append(data_1)
                    notice_list.append(data_2)
            else:
                for x in range(1, 3):
                    # 系部爬取两页
                    news_url = u'http://www.gdst.cc/' + \
                        self.option[key] + '/xbxw/xbdt/?page=' + str(x)
                    notice_url = u'http://www.gdst.cc/' + \
                        self.option[key] + '/xbxw/tzgg/?page=' + str(x)
                    data_1 = {
                        # 存储新闻URL
                        'origin': self.option[key],
                        'url': news_url,
                    }
                    data_2 = {
                        # 存储通告URL
                        'origin': self.option[key],
                        'url': notice_url,
                    }
                    news_list.append(data_1)
                    notice_list.append(data_2)

        return {'news': news_list, 'notice': notice_list}

    def get_list(self, list):
        news_list = []
        notice_list = []
        for url in list['news']:
            try:
                r = requests.get(url['url'])
                soup = BeautifulSoup(r.text, "html.parser")
                rows = soup.find(class_='article').find_all('li')
            except Exception as e:
                logging.warning(u'学院官网连接超时错误:%s' % e)
                return {}
            else:
                for row in rows:
                    date = row.find(class_='date')
                    # 匹配时间
                    if not date:
                        date = ''
                    else:
                        date = date.getText()
                        date.replace('/', '-')

                    title = row.a.string
                    url = row.a.attrs['href']
                    data = {
                        'title': title,
                        'url': u'http://www.gdst.cc/' + url,
                        'date': date,
                    }
                    print(data)
                    news_list.append(data)

        for url in list['notice']:
            try:
                r = requests.get(url['notice'])
                soup = BeautifulSoup(r.text, "html.parser")
                rows = soup.find(class_='article').find_all('li')
            except Exception as e:
                logging.warning(u'学院官网连接超时错误:%s' % e)
                return {}
            else:
                for row in rows:
                    date = row.find(class_='date')
                    # 匹配时间
                    if not date:
                        date = ''
                    else:
                        date = date.getText()
                        date.replace('/', '-')

                    title = row.a.string
                    url = row.a.attrs['href']
                    data = {
                        'title': title,
                        'url': u'www.gdst.cc/' + url,
                        'date': date,
                        'origin': url['origin']
                    }
                    print(data)
                    notice_list.append(data)
        return {
            'news': news_list,
            'notice': notice_list,
        }

    def get_detail(self, list):
        news_detail = []
        notice_detail = []
        for url in list['news']:
            try:
                r = requests.get(url['url'])
                soup = BeautifulSoup(r.text, 'html,parser')
                rows = soup.find(class_='articleinfor')
            except Exception as e:
                logging.warning(u'学院官网连接超时错误:%s' % e)
                return {}
            else:
                data = {
                    'title': url['title'],
                    'origin': url['origin'],
                    'html': rows,
                }
                news_detail.append(data)

        for url in list['notice']:
            try:
                r = requests.get(url['url'])
                soup = BeautifulSoup(r.text.'html.parser')
                rows = soup.find(class_='articleinfor')
            except Exception as e:
                logging.warning(u'学院官网连接超时错误:%s' % e)
                return {}
            else:
                data = {
                    'title': url['title'],
                    'origin': url['origin'],
                    'html': rows,
                }
                notice_detail.append(data)

        return{'news': news_detail, 'notice': notice_detail}

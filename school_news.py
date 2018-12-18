import requests
from bs4 import BeautifulSoup
import logging
import time
from decorator import  judge_list,judge_detail,new_cache

@judge_list()
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
        for n in range(1, 4):
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
            time.sleep(2)

    return {
        'data':news_list,
        'type':'news_list',
    }

@judge_list()
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
        for n in range(1, 4):
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
            time.sleep(2)

    return {
        'data':notice_list,
        'type':'notice_list',
    }


@judge_detail(get_news())
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
            }
            news_detail.append(data)
            time.sleep(2)

    return {
        'data':news_detail,
        'type':'news_detail',
    }


@judge_detail(get_notice())
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
            }
            notice_detail.append(data)
            time.sleep(2)

    return {
        'data':notice_detail,
        'type':'notice_detail'
    }

@new_cache()
def data_classify(dic):
    xy = []
    jsjx = []
    cjx = []
    ysx = []
    yyx = []
    jdx = []
    glx = []
    type = dic['type']
    list = dic['data']
    for data in list:
        if data['origin'] == "xy":
            xy.append(data)
        elif data['origin'] == "jsjx":
            jsjx.append(data)
        elif data["origin"] == "cjx":
            cjx.append(data)
        elif data["origin"] == "ysx":
            ysx.append(data)
        elif data["origin"] == "yyx":
            yyx.append(data)
        elif data['origin'] == "jdx":
            jdx.append(data)
        else:
            glx.append(data)

    return {
        'type':type,
        'xy':xy,
        'jsjx':jsjx,
        'cjx':cjx,
        'ysx':ysx,
        'yyx':yyx,
        'jdx':jdx,
        'glx':glx,
    }


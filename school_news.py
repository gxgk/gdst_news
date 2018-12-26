import requests
from bs4 import BeautifulSoup
import logging
import time
from fake_useragent import UserAgent
from base64 import b64encode
import re

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


def get_news(origin, page=1):
    # 获取新闻列表,接受前端的请求的来源（院别）,页数默认为1，新闻获取数量为15条
    url = 'http://www.gdust.cn/' + news_type[origin] + str(page)
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
        news_page = soup.find(class_='pageinfo').getText
        news_page = re.search(r"页次：(\d{1,2})\/", str(news_page))[1]
        if page == news_page:
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
                    'time': date,
                    'type': origin
                }
                news_list.append(data)
        else:
            return{}

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
        if rows:
            title = rows.find(class_="title").string
            date = rows.find(class_="info")
            date = re.search(r'\d.*\d', str(date))[0]
            content = rows.find(class_="content")
            content = str(content).replace(
                "src=\"/", "src=\"http://www.gdust.cn/")
            content = b64encode(content.encode())
    return {
        'title': title,
        'time': date,
        'html': bytes.decode(content),
    }

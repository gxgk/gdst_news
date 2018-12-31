import requests
from bs4 import BeautifulSoup
import logging
from base64 import b64encode
from urllib.parse import quote
import re
from all_cache import new_cache
import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)


news_type = {
    'xy': '/news/syyw/?page=',
    'jw': 'http://jwc.gdst.cc/jiaowuchu/index.aspx?lanmuid=94&sublanmuid=677&page=',
    '应用英语系': 'yyx/xbxw/xbdt/?page=',
    '计算机系': 'jsjx/xbxw/xbdt/?page=',
    '管理系': 'glx/xbxw/xbdt/?page=',
    '机电工程系': 'jdx/xbxw/xbdt/?page=',
    '艺术系': 'ysx/xbxw/xbdt/?page=',
    '财经系': 'cjx/xbxw/xbdt/?page=',
}


@new_cache('list')
def get_list_cache(origin, faculty, page):
    # 获取新闻列表,接受前端的请求的来源（院别）,页数默认为1，新闻获取数量为15条
    if origin == 'xy':
        url = 'http://www.gdust.cn/' + news_type[origin] + str(page)
    elif origin == 'jw':
        url = news_type[origin] + str(page)
    else:
        url = 'http://www.gdust.cn/' + news_type[faculty] + str(page)

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
        news_page = soup.find(class_='pageinfo').text
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
        '''
        else:
            return {}
        '''

    return news_list


@new_cache('detail')
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
            date = re.search('\d.*\d', str(date))[0]
            content = rows.find(class_="content")
            content = str(content).replace(
                "src=\"/", "src=\"http://www.gdust.cn/")
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
        headers = {'user-agent': ua.chrome}
        r = requests.get(url + '?lanmuid=94&sublanmuid=677', headers=headers)
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
                "src=\"/", "src=\"http://www.gdust.cn/")
            content = b64encode(content.encode())
    return {
        'title': title,
        'time': date,
        'html': bytes.decode(content),
    }


if __name__ == "__main__":
    for key in news_type:
        # 缓存列表
        if key not in ['xy', 'jw']:
            origin = 'xb'
            faculty = key
        else:
            origin = key
            faculty = ''

        for page in range(1, 6):
            get_list_cache(origin, faculty, page)
            time.sleep(2)

    for name in ['xb', 'jw', 'xy']:
        # 缓存详细
        data = r.hgetall(name)
        for value in data:
            if name is not 'jw':
                for url in value['url']:
                    get_news_detail(url)
                    time.sleep(1)
            else:
                for url in value['url']:
                    get_notice_detail(url)
                    time.sleep(1)

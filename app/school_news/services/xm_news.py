import requests
import logging
from app import redis_store
from bs4 import BeautifulSoup
import base64
import ast
from urllib.parse import quote,unquote

redis_plugin_prefix = 'wechat:plugins:news:xiaomiao'


def update_cache():
    url = 'http://mp.weixin.qq.com/mp/homepage' \
        '?__biz=MzI1MzA1MzQ0MA==&hid=3' \
        '&sn=2058fc67f54c5b913396dab4db8149ff'

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; ' +
        'Windows NT 6.2; Trident/6.0)'
    })
    try:
        res = session.get(url, timeout=6)
        url = url + '&begin=0&count=29&action=appmsg_list&f=json'
        res = session.post(url, timeout=6)
        appmsg_list = res.json()['appmsg_list']
    except Exception as e:
        logging.warning(u'连接超时出错：%s' % e)
        return {}
    news_list = []
    for appmsg in appmsg_list:
        news_data = {
            "title": appmsg['title'],
            "url": quote(appmsg['link']),
            "type": "xm",
        }
        news_list.append(news_data)

        redis_store.set(redis_plugin_prefix + ':list', news_list, 3600 * 10)


def get_list(page=1):
    page = int(page)
    if page >= 3:
        return {'end': ''}
    list_cache = redis_store.get(redis_plugin_prefix + ':list')
    if not list_cache:
        update_cache()
        list_cache = redis_store.get(redis_plugin_prefix + ':list')
    cache = ast.literal_eval(str(list_cache, encoding='utf-8'))
    cache_list = []
    for i in range(0, len(cache), 10):
        cache_list.append(cache[i:i + 10])
    return cache_list[page - 1]


def get_detail(url):
    return {
        'status':200,
        'url':unquote(url)
    }

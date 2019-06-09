import requests
import logging
from app import redis_store
import pickle
from urllib.parse import quote,unquote

redis_plugin_prefix = 'wechat:plugins:news:xiaomiao'


def update_cache():
    urls = ['http://mp.weixin.qq.com/mp/homepage?__biz=MzI1MzA1MzQ0MA==&' \
          'hid=3&sn=2058fc67f54c5b913396dab4db8149ff&begin=0&count=29&action=appmsg_list&f=json',
           'https://mp.weixin.qq.com/mp/homepage?__biz=MzU1NDkwNDY5MQ==&'\
           'hid=1&sn=d19338069924da83163881e59cc771ca&begin=0&count=29&action=appmsg_list&f=json'
           ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; ' +
        'Windows NT 6.2; Trident/6.0)'
    }
    news_list = []
    for url in urls:
        try:
            res = requests.get(url, timeout=6, headers=headers)
            appmsg_list = res.json()['data']['homepage_render']['appmsg_list']
        except Exception as e:
            logging.warning(u'连接超时出错：%s' % e)
            return {}

        for appmsg in appmsg_list:
            news_data = {
                "title": appmsg['title'],
                "url": quote(appmsg['link']),
                "author": appmsg['author'],
                "type": "xm",
            }
            news_list.append(news_data)
    redis_store.set(redis_plugin_prefix, pickle.dumps(news_list), 3600 * 10)
    return news_list


def get_list(page, force_reload=False):
    list_cache = redis_store.get(redis_plugin_prefix)
    if list_cache and force_reload is False:
        cache_list = pickle.loads(list_cache)
    else:
        cache_list = update_cache()
    return cache_list


def get_detail(url):
    return {
        'status': 200,
        'url': unquote(url)
    }

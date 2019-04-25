import logging
import config
import wechatsogou
import pickle
import json
from urllib.parse import quote
from app.extensions import redis_store
from utils import rk


def xm_news_list(page, force_reload=False):
    article_list = []
    for mp_name in config.MP_ARTICLE_LIST:
        cache_key = "cache_mp_article?mp_name=%s" % mp_name
        page_size = config.PAGE_SIZE
        data_list = redis_store.zrevrange(cache_key, (page - 1) * page_size, page * page_size - 1)
        if (not data_list and page <= 1) or force_reload is True:
            cache_mp_article(mp_name)
            data_list = redis_store.zrevrange(cache_key, (page - 1) * page_size, page * page_size - 1)
        for data in data_list:
            article_list.append(json.loads(data))
    return article_list


def crawler_mp_article(gzh_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
    }
    ws_api = wechatsogou.WechatSogouAPI(
        headers=headers,
        captcha_break_time=3,
        timeout=5)
    news_list = []
    try:
        history = ws_api.get_gzh_article_by_history(gzh_name,
                                                    identify_image_callback_sogou=rk.identify_image_callback_ruokuai_sogou,
                                                    identify_image_callback_weixin=rk.identify_image_callback_ruokuai_weixin)
        if not history:
            return None
        gzh = history.get('gzh')
        history_list = history.get('article')
    except Exception as e:
        logging.warning(u'无法爬取到公众号文章列表:%s' % e)
        return None
    else:
        for n, history in enumerate(history_list):
            news = {
                'type': 'xm',
                'title': history['title'],
                'url': quote(history['content_url']),
                'author': gzh.get('wechat_name'),
                'datetime': history['datetime']
            }
            news_list.append(news)

    return news_list


def cache_mp_article(mp_name):
    data_list = crawler_mp_article(mp_name)
    if not data_list:
        return None
    cache_key = "cache_mp_article?mp_name=%s" % mp_name

    # 删除全部旧数据
    redis_store.delete(cache_key)
    mapping = {}
    for data in data_list:
        mapping.update({json.dumps(data): data['datetime']})
    redis_store.zadd(cache_key, mapping)

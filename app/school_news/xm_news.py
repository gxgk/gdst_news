import wechatsogou
import logging
import config
from urllib.parse import quote
from . import rk


def xm_news_list():
    ws_api = wechatsogou.WechatSogouAPI(
        captcha_break_time=3,
        timeout=5
    )
    news_list = []
    for gzh_name in config.GZH_LIST:
        try:
            history_list = ws_api.get_gzh_article_by_history(gzh_name,
                identify_image_callback_sogou=rk.identify_image_callback_ruokuai_sogou,
                identify_image_callback_weixin=rk.identify_image_callback_ruokuai_weixin)
        except Exception as e:
            logging.warning(u'无法爬取到公众号文章列表:%s' % e)
            return {}
        else:
            if history_list:
                for n in range(0, 3):
                    news = {
                        'type': 'xm',
                        'title': history_list['article'][n]['title'],
                        'url': quote(
                            history_list['article'][n]['content_url']),
                        'time': history_list['gzh']['wechat_name']}
                    news_list.append(news)

    if news_list:
        return news_list
    else:
        return{}


def xm_news_detail(url):
    '''
    try:
        r = requests.get(url)
    except Exception as e:
        logging.warning(u'无法爬取到文章详细:%s' % e)
        return {}
    else:
        soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
        rows = soup.find(class_='rich_media_area_primary_inner')
        title = rows.h2.string
        author = rows.a.string
        title = str(title).replace('\n','')
        title = str(title).replace(' ','')
        author = str(author).replace('\n','')
        author = str(author).replace(' ','')
        content = rows.find(class_='rich_media_content')
        content = b64encode(content.encode())
        html = bytes.decode(content)

        return {}
'''

    return {'url': url}


if __name__ == "__main__":
    news_list = xm_news_list()
    content = xm_news_detail(news_list[0])
    print(content)

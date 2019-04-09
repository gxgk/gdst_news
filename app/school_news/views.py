from flask import request
import json
from app.school_news import school_news
from app.school_news import xm_news
from urllib.parse import unquote
from . import school_news_mod


@school_news_mod.route('/news/list', methods=['GET'])
def get_list_api():
    news_type = request.args.get('news_type')
    page = request.args.get('page')
    faculty = request.args.get('faculty')
    faculty = unquote(faculty)
    gzh_name = request.args.get('gzh_name')
    force_reload = request.args.get('force_reload')
    if force_reload == '1':
        force_reload = True
    else:
        force_reload = False
    # 获取新闻或通告列表
    if news_type not in ['all', 'xm']:
        list = school_news.get_news(news_type, faculty, page, force_reload)
    elif news_type == 'xm':
        if int(page) >= 2:
            return json.dumps({
                'status': 200,
                'data': '',
            })
        else:
            list = xm_news.xm_news_list(gzh_name)
    else:
        #list_1 = xm_news.xm_news_list(['广科严选'])
        list = school_news.get_headline(faculty, page, force_reload)
        #list = list_1 + list_2

    return json.dumps({
        'status': 200,
        'data': list,
    })


@school_news_mod.route('/news/detail', methods=['GET'])
# 接受新闻内容URL
def get_detail_api():
    url = request.args.get('url')
    # 获取新闻或者通告详细
    news_type = request.args.get('type')
    url = unquote(url)
    force_reload = request.args.get('force_reload')
    if news_type == 'jw':
        detail = school_news.get_notice_detail(url, force_reload)
    elif news_type == 'xm':
        detail = xm_news.xm_news_detail(url)
    else:
        detail = school_news.get_news_detail(url, force_reload)

    return json.dumps({'status': 200, 'data': detail})

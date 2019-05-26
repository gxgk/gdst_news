from flask import request
import json
from app.school_news import school_news
from app.school_news.services import xm_news
from urllib.parse import unquote
from . import school_news_mod


@school_news_mod.route('/news/list', methods=['GET'])
def get_list_api():
    news_type = request.args.get('news_type')
    page = request.args.get('page')
    faculty = request.args.get('faculty')
    faculty = unquote(faculty)
    force_reload = request.args.get('force_reload', 0, type=int)
    # 获取新闻或通告列表
    if news_type not in ['all', 'xm']:
        list = school_news.get_news(
            news_type, faculty, page, bool(force_reload))
    elif news_type == 'xm':
        if page != '1':
            return json.dumps({
                'status': 200,
                'data': ''
            })
        else:
            list = xm_news.get_list(page, bool(force_reload))
    else:
        list = school_news.get_headline(faculty, page)

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
    force_reload = request.args.get('force_reload', 0, type=int)
    if news_type == 'jw':
        url = unquote(url)
        detail = school_news.get_notice_detail(url, bool(force_reload))
    elif news_type == 'xm':
        detail = xm_news.get_detail(url)
    else:
        url = unquote(url)
        detail = school_news.get_news_detail(url, bool(force_reload))

    return json.dumps({'status': 200, 'data': detail})

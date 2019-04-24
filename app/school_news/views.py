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
    force_reload = request.args.get('force_reload', 0, type=int)
    # 获取新闻或通告列表
    if news_type not in ['all', 'xm']:
        list = school_news.get_news(
            news_type, faculty, page, bool(force_reload))
    elif news_type == 'xm':
        list = xm_news.xm_news_list(gzh_name,page)
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
    url = unquote(url)
    force_reload = request.args.get('force_reload', 0, type=int)
    if news_type == 'jw':
        detail = school_news.get_notice_detail(url, bool(force_reload))
    elif news_type == 'xm':
        detail = xm_news.xm_news_detail(url)
    else:
        detail = school_news.get_news_detail(url, bool(force_reload))

    return json.dumps({'status': 200, 'data': detail})

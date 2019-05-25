from flask import request, jsonify
import json
from app.school_news import school_news
from app.school_news.services import xm_news
from urllib.parse import unquote
from . import school_news_mod


@school_news_mod.route('/news/list', methods=['GET'])
def get_list_api():
    news_type = request.args.get('news_type', type=str)
    page = request.args.get('page', type=int)
    faculty = request.args.get('faculty', type=str)
    force_reload = request.args.get('force_reload', 0, type=int)
    force_reload = bool(force_reload)
    # 获取新闻或通告列表
    if news_type not in ['all', 'xm']:
        news_list = school_news.get_news(
            news_type, faculty, page, force_reload)
    elif news_type == 'xm':
        news_list = xm_news.get_list()
    else:
        news_list = school_news.get_headline(faculty, page)

    return jsonify({
        'status': 200,
        'data': news_list,
    })


@school_news_mod.route('/news/detail', methods=['GET'])
# 接受新闻内容URL
def get_detail_api():
    url = request.args.get('url')
    news_id = request.args.get('articleid')
    # 获取新闻或者通告详细
    news_type = request.args.get('type')
    force_reload = request.args.get('force_reload', 0, type=int)
    if news_type == 'jw':
        url = unquote(url)
        detail = school_news.get_notice_detail(url, bool(force_reload))
    elif news_type == 'xm':
        detail = xm_news.get_detail(news_id)
    else:
        url = unquote(url)
        detail = school_news.get_news_detail(url, bool(force_reload))

    return json.dumps({'status': 200, 'data': detail})

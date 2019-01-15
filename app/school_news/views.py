from flask import request
import json
from app.school_news import school_news
from urllib.parse import unquote
import re
from . import school_news_mod


@school_news_mod.route('/news/list', methods=['GET'])
def get_list_api():
    news_type = request.args.get('news_type')
    page = request.args.get('page')
    faculty = request.args.get('faculty')
    faculty = unquote(faculty)
    # 获取新闻或通告列表
    if news_type != 'all':
        list = school_news.get_news(news_type, faculty, page)
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
    url = unquote(url)
    try:
        if re.search('http://jwc.gdst.cc/', url)[0]:
            detail = school_news.get_notice_detail(url)
    except BaseException:
        detail = school_news.get_news_detail(url)

    return json.dumps({'status': 200, 'data': detail})

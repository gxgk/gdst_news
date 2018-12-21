from flask import Flask, request
import json
import school_news as sn


app = Flask(__name__)


@app.route('/<type>/<origin>', methods=['GET'])
def get_list_api(type, origin):
    page = request.args.get('page')
    # 获取新闻或通告列表
    if type == 'news':
        list = sn.get_news(origin, page)
    else:
        list = sn.get_notice(origin, page)

    return json.dumps(list)


@app.route('/<type>/<origin>/<url>', methods=['GET'])
# 接受新闻内容URL
def get_detail_api(type, origin, url):
    # 获取新闻或者通告详细
    if type == "news":
        detail = sn.get_news_detail(url)
    if type == "notice":
        detail = sn.get_notice_detail(url)

    return json.dumps(detail)

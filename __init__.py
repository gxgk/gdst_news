from flask import Flask, request
import json
import school_news as sn
from urllib.parse import unquote
import re
app = Flask(__name__)


@app.route('/news/list', methods=['GET'])
def get_list_api():
    news_type = request.args.get('news_type')
    page = request.args.get('page')
    # 获取新闻或通告列表
    list = sn.get_news(news_type, page)
    return json.dumps({'status': 200, 'data': list})


@app.route('/news/detail', methods=['GET'])
# 接受新闻内容URL
def get_detail_api():
    url = request.args.get('url')
    # 获取新闻或者通告详细
    url = unquote(url)
    try:
        if re.search('http://jwc.gdst.cc/', url)[0]:
            detail = sn.get_notice_detail(url)
    except BaseException:
        detail = sn.get_news_detail(url)

    return json.dumps({'status': 200, 'data': detail})


if __name__ == "__main__":
    app.run(debug=True)

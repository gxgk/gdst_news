from flask import Flask
import json
from . import school_news as sn

app = Flask(__name__)


@app.route('/api/SearchBook', methods=['GET'])
def spider():
    news_detail = sn.get_news_detail(sn.get_news())
    notice_detail = sn.get_notice_detail(sn.get_notice())

    return json.dump({
        'news_detail': news_detail,
        'notice_detail': notice_detail,
    })

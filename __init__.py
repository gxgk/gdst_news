from flask import Flask
import json
import school_news as sn
import redis
from flask import request


app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def spider():
    news_list = sn.get_news()
    notice_list = sn.get_notice()
    news_detail = sn.get_news_detail(news_list)
    notice_detail = sn.get_notice_detail(notice_list)

    sn.data_classify(news_list)
    sn.data_classify(notice_list)
    sn.data_classify(news_detail)
    sn.data_classify(notice_detail)

@app.route('/result/<type>/page=<page>',method="GET")
def return_result(type,page):
    if request.method == "GET":
        m = int(page)*10-10
        n = int(page)*10-1
        try:
            data = r.get('type')[m:n]
            return json.dumps({
                'data':data,
                'content':'上滑获取更多'
            })
        except:
            if r.get('type')[m] is False:
                return json.dumps({'data':'没有再多的了！'})
            else:
                while r.get('type')[m]:
                    m+=1

                data = r.get('type')[n:m-1]
                return json.dumps({
                    'data': data,
                    'content': '没有再多的了！'
                })







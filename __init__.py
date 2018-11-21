from flask import Flask
import json
import school_news as sn
import redis


app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
r = redis.Redis(connection_pool=pool)


@app.route('/api/GetNews', methods=['GET'])
def spider():
    news_detail = sn.get_news_detail()
    notice_detail = sn.get_notice_detail()
    return json.dumps({
        'news_dateil':news_detail,
        'notice_dateil'notice_detail,
    })

if __name__ == '__main__':
    app.run(debug=True,port=8848)

from flask import Flask
import json
import school_news as sn
import redis


app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


@app.route('/api/GetNews', methods=['GET'])
def spider():
    news_list = sn.get_news()
    notice_list = sn.get_notice()
    news_detail = sn.get_news_detail(news_list)
    notice_detail = sn.get_notice_detail(notice_list)
    xy_newslist = []
    xy_newsdetail = []

    for content in news_list:
        if content['origin'] == 'xy':
            xy_newslist.append(content)
            news_list.remove(content)

    for content in news_detail:
        if content['origin'] == 'xy':
            xy_newsdetail.append(content)
            news_list.remove(content)

    return json.dumps({
        'xy_news_list':xy_newslist,
        'xy_news_detail':xy_newsdetail,
        'orther_news':news_list,
        'notice_list':notice_list,
        'notice_detail':notice_detail,
    })

if __name__ == '__main__':
    app.run(debug=True, port=8848)

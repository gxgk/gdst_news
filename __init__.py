from flask import Flask, jsonify
import school_news as sn


app = Flask(__name__)


@app.route('/api/GetNews', methods=['GET'])
def spider():
    news_detail = sn.get_news_detail(sn.get_news())
    notice_detail = sn.get_notice_detail(sn.get_notice())

    return ({
        'news_detail': news_detail,
        'notice_detail': notice_detail,
    })


if __name__ == '__main__':
    app.run(debug=True)

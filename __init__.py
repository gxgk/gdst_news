from flask import Flask
import json
import school_news as sn


app = Flask(__name__)


@app.route('/api/GetNews', methods=['GET'])
def spider():
    return json.dumps({'code':'hello word'})

if __name__ == '__main__':
    app.run(debug=True,port=8848)

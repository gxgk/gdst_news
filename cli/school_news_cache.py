import requests
import time
from ast import literal_eval

news_type = {
    'xy': '/news/syyw/?page=',
    'jw': 'http://jwc.gdst.cc/jiaowuchu/index.aspx?lanmuid=94&sublanmuid=677&page=',
    '应用英语系': 'yyx/xbxw/xbdt/?page=',
    '计算机系': 'jsjx/xbxw/xbdt/?page=',
    '管理系': 'glx/xbxw/xbdt/?page=',
    '机电工程系': 'jdx/xbxw/xbdt/?page=',
    '艺术系': 'ysx/xbxw/xbdt/?page=',
    '财经系': 'cjx/xbxw/xbdt/?page=',
}


def main():
    for key in news_type.keys():
        # 缓存列表
        if key not in ['xy', 'jw']:
            origin = 'xb'
            faculty = key
        else:
            origin = key
            faculty = ''

        for page in range(1, 6):
            ret = requests.get(
                "http://127.0.0.1:5000/news/list?news_type=%s&page=%s&faculty=%s" %
                (origin, page, faculty))
            data = bytes.decode(ret.content)
            for content in literal_eval(data)['data']:
                url = content['url']
                r = requests.get(
                    "http://127.0.0.1:500/news/detail?type=%s&url=%s" %
                    (origin, url))
                time.sleep(1)
            time.sleep(1)


if __name__ == '__main__':
    main()

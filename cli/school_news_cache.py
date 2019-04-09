import sys
import os

project = os.path.abspath(os.path.dirname(os.getcwd()))  # 工作项目根目录
sys.path.append(os.getcwd().split(project)[0] + project)

import requests
import time
from ast import literal_eval
import config

def main():
    for key in config.NEWS_TYPE.keys():
        # 缓存列表
        if key not in ['xy', 'jw']:
            origin = 'xb'
            faculty = key
        else:
            origin = key
            faculty = ''

        for page in range(1, 6):
            ret = requests.get(
                "%s?news_type=%s&page=%s&faculty=%s&force_reload=%s" %
                (config.LIST_URL, origin, page, faculty,'1'))
            data = bytes.decode(ret.content)
            for content in literal_eval(data)['data']:
                url = content['url']
                requests.get(
                    "%s?type=%s&url=%s&force_reload=%s" %
                    (config.DETAIL_URL, origin, url,'1'))
                print(url)
                time.sleep(1)
            time.sleep(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import config
import time
import ast
from app import create_app

app = create_app()


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_requests(self):
        for key in config.NEWS_TYPE.keys():
            # 缓存列表
            if key not in ['xy', 'jw','xm']:
                origin = 'xb'
                faculty = key
            else:
                origin = key
                faculty = ''

            for page in range(1, 1):
                qurey_url = "%s?news_type=%s&page=%s&faculty=%s&request_type=%s" %(config.LIST_URL, origin, page, faculty,'test')
                if key == 'xm':
                    for gzh_name in config.NEWS_TYPE['xm']:
                        qurey_url += '&gzh_name=%s' % gzh_name
                        self.app.get(qurey_url)
                        print(qurey_url)
                else:
                    ret = self.app.get(qurey_url)
                    data = bytes.decode(ret.data)
                    print(qurey_url)
                    for content in ast.literal_eval(data)['data']:
                        url = content['url']
                        self.app.get(
                            "%s?type=%s&url=%s" %
                            (config.DETAIL_URL, origin, url))
                        print(url)
                        time.sleep(1)
                    time.sleep(1)





if __name__ == '__main__':
    with app.app_context():
        unittest.main()

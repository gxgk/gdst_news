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
            if key not in ['xy', 'jw', 'xm']:
                origin = 'xb'
                faculty = key
            else:
                origin = key
                faculty = ''

            for page in range(1, 2):
                qurey_url = "%s?news_type=%s&page=%s&faculty=%s&force_reload=%s" % (
                    config.LIST_URL, origin, page, faculty, '1')
                ret = self.app.get(qurey_url)
                data = bytes.decode(ret.data)
                print(qurey_url)
                for content in ast.literal_eval(data)['data']:
                    url = content['url']
                    if origin == 'xm':
                        self.app.get(
                        "%s?type=%s&url=%s&articleid=%s&force_reload=%s" %
                        (config.DETAIL_URL, origin, url,content['articleid'], '1'))
                    else:
                        self.app.get(
                            "%s?type=%s&url=%s&force_reload=%s" %
                            (config.DETAIL_URL, origin, url, '1'))
                    print(url)
                    time.sleep(1)
                time.sleep(1)


if __name__ == '__main__':
    with app.app_context():
        unittest.main()

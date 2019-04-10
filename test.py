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
                qurey_url_test = "%s?news_type=%s&page=%s&faculty=%s&force_reload=%s" % (
                    config.LIST_URL, origin, page, faculty, '1')

                qurey_url = "%s?news_type=%s&page=%s&faculty=%s" %(config.LIST_URL, origin, page, faculty)
                if key == 'xm':
                    for gzh_name in config.NEWS_TYPE['xm']:
                        qurey_url += '&gzh_name=%s' % gzh_name
                        qurey_url_test += '&gzh_name=%s' % gzh_name
                        self.app.get(qurey_url)
                        self.app.get(qurey_url_test)
                        print(qurey_url)
                        print(qurey_url_test)
                else:
                    ret = self.app.get(qurey_url)
                    ret_test = self.app.get(qurey_url_test)
                    data = bytes.decode(ret.data)
                    data_test = bytes.decode(ret_test.data)
                    print(qurey_url)
                    print(qurey_url_test)
                    for content in ast.literal_eval(data)['data']:
                        url = content['url']
                        self.app.get(
                            "%s?type=%s&url=%s&force_reload=%s" %
                            (config.DETAIL_URL, origin, url, '1'))
                        print(url)
                        time.sleep(1)
                    time.sleep(1)

                    for content in ast.literal_eval(data_test)['data']:
                        url = content['url']
                        self.app.get(
                            "%s?type=%s&url=%s&force_reload=%s" %
                            (config.DETAIL_URL, origin, url, '1'))
                        print(url)
                        time.sleep(1)
                    time.sleep(1)


if __name__ == '__main__':
    with app.app_context():
        unittest.main()

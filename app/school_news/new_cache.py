import re
import ast

from app import redis_store


def new_cache(storage_type, *args, **kwargs):
    # storage_type 为储存类型 'list','detail','cache'
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_data = [data for data in args]
            #args_data = ['origin','faculty','page']
            '''
            若是获取LIST，参数为 origin,faculty,page
            若是获取DETAIL，参数为 url

            '''
            if storage_type == 'list':
                # 缓存新闻列表
                name = args_data[0]
                # origin
                if name in ['xy', 'jw']:
                    # 将xy,jw与xb区分,方便进行缓存
                    key = args_data[2]
                    # page
                else:
                    key = args_data[1] + "_" + args_data[2]
                    # faculty_page
                data = redis_store.hget(name, key)
                if data:
                    data = ast.literal_eval(bytes.decode(data))
                    return data
                else:
                    data = func(*args, **kwargs)
                    redis_store.hset(name, key, str(data))
                    redis_store.expire(name, 86400)
                    # 缓存过期时间为一天
            elif storage_type == 'detail':
                # 缓存新闻详细
                url = args[0]
                # url
                result_1 = re.search('http://(.*?)/', url)
                # 用于判断是是否是教务处新闻详细
                if result_1[1] == 'www.gdust.cn':
                    result_2 = re.search('(\d{8})\/(\d{1,4})', url)
                    kw = result_2[1] + result_2[2]
                else:
                    kw = re.search('\&id\=(\d{1,3})', url)[1]

                data = redis_store.get(kw)
                if not data:
                    data = func(*args, **kwargs)
                    redis_store.set(kw, str(data))
                    redis_store.expire(kw, 86400)
                else:
                    data = ast.literal_eval(bytes.decode(data))
                    return data

            return data
        return wrapper
    return decorator

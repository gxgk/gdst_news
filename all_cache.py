import re
import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)

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
                    key = args_data[1] + "_" + str(args_data[2])
                    # faculty_page

                data = func(*args, **kwargs)
                r.hset(name, key, data)
                r.expire(name, 86400)
                # 缓存过期时间为一天
            elif storage_type == 'detail':
                # 缓存新闻详细
                url = args[0]
                # url
                result_1 = re.search('http://(.*?)/', url)
                # 用于判断是是否是教务处新闻详细
                if result_1[1] == 'www.gdst.cc':
                    result_2 = re.search('(\d{8})\/(\d{4})', url)
                    kw = result_2[1] + result_2[2]
                else:
                    kw = re.search('id\=(\d{1,3})', url)[1]

                data = func(*args, **kwargs)
                r.set(kw, data,)
                r.expire(kw, 86400)

            return data
        return wrapper
    return decorator

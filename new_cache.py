import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)


def new_cache(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_data = [data for data in args]

            if len(args_data) == 3:
                name = args_data[0]
                # origin
                if name == 'xy' or name == 'jw':
                    key = args_data[2]
                    # page
                else:
                    key = args_data[1] + '_' + args_data[2]
                    # faculty_page
                data = r.hget(name, key)
                if data == False or data == None:
                    data = func(*args, **kwargs)
                    r.hset(name, key, data)
                    r.expire(name, 86400)
                    # 缓存过期时间为一天
                else:
                    data = eval(data)
                    return data

            else:
                url = args[0]
                # url
                result_1 = re.search('http://(.*?)/', url)
                # 用于判断是是否是教务处新闻详细
                if result_1[1] == 'www.gdst.cc':
                    result_2 = re.search(r'(\d{8})\/(\d{4})', url)
                    kw = result_2[1] + result_2[2]
                else:
                    kw = re.search(r'id\=(\d{1,3})', url)[1]

                data = r.get(kw)
                if data == False or data == None:
                    data = func(*args, **kwargs)
                    r.set(kw, data,)
                    r.expire(kw, 86400)
                else:
                    data = eval(data)
                    return data

            return data
        return wrapper
    return decorator

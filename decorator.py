import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


def judge_list():
    # 检查判断函数是否执行
    def decorator(func):
        def wrapper(*args, **kw):
            if r.get('xy_news_list') is None or r.exists('xy_news_list') is False:
                data = func()
                return data
            else:
                return 'data is already'
        return wrapper
    return decorator

def judge_detail(data):
    def decorator(func):
        def wrapper(*args,**kw):
            if data != 'data is already':
                if r.get("xy_news_detail") is None or r.exists('xy_news_detail') is False:
                    content = func(data)
                    return content
            else:
                return 'data is already'
        return wrapper
    return decorator

def new_cache(dic):
    def decorator(func):
        def wrapper(*args, **kw):
            data = func(dic)
            type = data['type']
            del data['type']
            for key in data:
                r.set(key +'_'+ type, data[key], ex=60 * 4320)
        return warpper
    return decorator

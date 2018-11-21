import redis
import re

pool = redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
r = redis.Redis(connection_pool=pool)

def new_cache():
    def decorator(func):
        def wrapper(*args, **kw):
            if r.get(func.__name__) is None or r.exists(func.__name__) is False:
                #判断是否是第一次缓存或者缓存过期
                if re.search('(detail)',func.__name__) is None:
                    data = func()
                    r.set(func.__name__,str(data),ex=60*2880)
                    #列表缓存2天
                else:
                    title = re.search('get_(.*)_detail',func.__name__)
                    data = func(eval(r.get('get_'+title.group(1))))
                    r.set(func.__name__,str(data),ex=60*4320)
                    #详细缓存3天

            else:
                return

            return data
        return wrapper
    return decorator

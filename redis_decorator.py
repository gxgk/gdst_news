import redis
import re


def new_cache():
    def decorator(func):
        def wrapper(*args, **kw):
            if func.__name__ == 'get_news' or func.__name__ == 'get_notice':
                # 判断是获取列表函数还是详细函数
                if r.get(
                        func.__name__) is None or r.exists(
                        func.__name__) is False:
                    # 判断是否是第一次缓存或缓存已经过期
                    data = func()
                    r.set(func.__name__ + 'old', str(data), ex=60 * 2880)
                    # 列表缓存时间为2天
                else:
                    # 判断有无新增
                    data = func()
                    old_list = eval(r.get(func.__name__ + 'old'))
                    if data != old_list:
                        r.set(func.__name__ + 'new', str(data), ex=60 * 2880)

            elif func.__name__ == 'get_news_detail':
                if r.get(
                        func.__name__) is None or r.exists(
                        func.__name__) is False:
                    data = func(eval(r.get('get_newsnew')))
                    r.set(func.__name__, str(data), ex=60 * 4320)
                    # 详细缓存三天
                else:
                    # 判断有无新增
                    new = eval(r.get('get_newsnew'))
                    old = eval(r.get('get_newsold'))
                    if new != old:
                        data = func(new)
                        r.set(func.__name__, str(data), ex=60 * 4320)
                    else:
                        data = eval(r.get(func.__name__))

            else:
                if r.get(
                        func.__name__) is None or r.exists(
                        func.__name__) is False:
                    data = func(eval(r.get('get_noticesnew')))
                    r.set(func.__name__, str(data), ex=60 * 4320)
                    # 详细缓存三天
                else:
                    new = eval(r.get('get_noticenew'))
                    old = eval(r.get('get_noticeold'))
                    if new != old:
                        data = func(new)
                        r.set(func.__name__, str(data), ex=60 * 4320)
                    else:
                        data = eval(r.get(func.__name__))

            return data
        return wrapper
    return decorator

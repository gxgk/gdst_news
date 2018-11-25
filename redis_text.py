import redis
import re


def new_cache():
    def decorator(func):
        def wrapper(*args, **kw):
            if func.__name__ == 'get_news' or func.__name__ == 'get_notice':
                if r.get(
                        func.__name__ +
                        'xy') is None or r.exists(
                        func.__name__ +
                        'xy'):
                    # 判断缓存是否过期或是否是第一次缓存
                    data = func()
                    r.set('old_list', str(data))
                    r.expire('old_list', 60 * 2880)
                    # 储存data集合 用于验证是否有新增与get_xxx_detail函数使用
                    for content in data:
                        r.lpush(
                            func.__name__ +
                            content['origin'],
                            str(content))
                        r.expire(func.__name__ + content['origin', 60 * 2880])
                        # 列表缓存时间为两天

                data = func()
                if data != eval(r.get('list')):
                    r.set('new_list', str(data))
                    r.expire('new_list', 60 * 2880)
                # 判断是否有新增
                    for content not in data:
                        list = r.get(func.__name__ + content['origin'])
                        r.lpush(
                            func.__name__ +
                            content['origin'],
                            str(content))
                        r.expire(func.__name__ + content['origin'], 60 * 2880)

            else:
                if r.get(
                        func.__name__ +
                        'xy') is None or r.exists(
                        func.__name__ +
                        'xy') or r.get('old_list') != r.get('new_list'):
                    # 若old_list与new_list不相同则表示有新增内容 也重新获取
                    data = func(eval(r.get('new_list')))
                    for content in data:
                        r.lpush(
                            func.__name__ +
                            content['origin'],
                            str(content))
                        r.expire(func.__name__ + content['origin'], 60 * 4320)
                        # 详细缓存时间为三天

            return data
        return wrapper
    return decorator

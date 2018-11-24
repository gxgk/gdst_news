import redis
import re


def new_cache():
    def decorator(func):
        def wrapper(*args, **kw):
            if r.get(
                    func.__name__ +
                    'xy') is None or r.exists(
                    func.__name__ +
                    'xy'):
                # 判断缓存过期或者第一次缓存
                if func.__name__ == 'get_news' or func.__name__ == 'get_notice':
                    data = func()
                    r.set(func.__name__ + '_list', str(data))
                    for content in data:
                        r.rpush(
                            func.__name__ +
                            content['origin'],
                            str(content))
                        r.expire(func.__name__ + content['origin'], 60 * 2880)
                        # 列表缓存过期时间为两天
                else:

                    data = func(eval(r.get(func.__name__ + 'list')))
                    for content in data:
                        r.rpush(
                            func.__name__ +
                            content['origin'],
                            str(content))
                        r.expire(func.__name__ + content['origin'], 60 * 2880)
                        # 详细缓存过期时间为三天

            else:
                # 若缓存为过期则判断有无新增
                if func.__name__ == 'get_news'or func.__name__ == 'get_notice':
                    data = func()
                try:
                    # 只有当被修饰的函数是get_news()或get_notice()才执行
                    for content in data:
                        old_list = r.get(func.__name__ + content['origin'])
                        if content not in old_list:
                            r.rpush(
                                func.__name__ +
                                content['origin'],
                                str(content))

                except BaseException:
                    pass

                else:
                    data = []
                    for type in [
                        'xy',
                        'jxjx',
                        'cjx',
                        'ysx',
                        'yyx',
                        'glx',
                        'jdx',
                    ]:
                        data.append(eval(r.get(func.__name__ + type)))

            return data
        return wrapper
    return decorator

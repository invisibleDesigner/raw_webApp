import time
import random
from datetime import datetime


def log(*args, **kwargs):
    """导出日志"""
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('web.log', mode='a+', encoding='utf-8') as f:
        print(dt, *args, **kwargs, file=f)


def formatted_time():
    dt = datetime.now()
    ds = dt.strftime('%Y-%m-%d %H:%M:%S')
    return ds


def unformatted_time(t):
    st = time.strptime(t, '%Y-%m-%d %H:%M:%S')
    tt = time.mktime(st)
    return tt


def random_string():
    seed = 'abcdefghijklgmopqrstuvwxyz'
    s = ''
    for i in range(16):
        s += random.choice(seed)
    return s

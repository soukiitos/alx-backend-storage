#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker'''
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    '''Define get_page'''
    if url is None or len(url.strip()) == 0:
        return ''
    redis_store = redis.Redis()
    key = 'result:{}'.format(url)
    request = 'count:{}'.format(url)
    result = redis_store.get(key)
    if result is not None:
        redis_store.incr(request)
        return result
    result = requests.get(url).content.decode('utf-8')
    redis_store.setex(key, int(timedelta(seconds=10).total_seconds()), result)
    return result

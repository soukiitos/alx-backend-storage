#!/usr/bin/env python3
'''Writing strings to Redis'''
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    '''Define count_calls'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Define wrapper'''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Define call_history'''
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Define wrapper'''
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def replay(method: Callable) -> None:
    '''Define replay'''
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, j in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            name, i.decode('utf-8'), j.decode('utf-8')
            ))


class Cache:
    '''Create Cache class'''
    def __init__(self) -> None:
        '''Define __init__'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Define store'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        '''Define get'''
        data = self._redis.get(key)
        if data is not None:
            if fn is not None:
                if fn == int:
                    raise ValueError("Cannot apply int() conversion")
                elif Callable(fn):
                    return fn(data)
            return data

    def get_str(self, key: str) -> str:
        '''Define get_str'''
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        '''Define get_int'''
        data = self

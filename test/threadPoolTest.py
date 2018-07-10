# -*- coding:utf8 -*-
import threadpool

from common.base import log, consoleLog, Base
from common import sqlbase
import time

class A(object):

    _a = None

    @classmethod
    def set_a(cls, x):
        cls._a = x

    @classmethod
    def get_a(cls):
        return cls._a

a1 = A()
a2 = A()

print a1.get_a()
a1.set_a('233')
print a2.get_a()


def fun(i):
    print i
    time.sleep(1)

def num():
    a = []
    for i in range(100):
        a.append(i)
    return a

# L = num()
# pool = threadpool.ThreadPool(20)
# requests = threadpool.makeRequests(fun, L)
# [pool.putRequest(req) for req in requests]
# pool.wait()

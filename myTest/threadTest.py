# -*- coding:utf8 -*-
from random import randrange

from common.base import log, consoleLog, Base
from common import sqlbase
import time
from threading import Thread, Lock
import thread
from threading import currentThread

Lock()

def test(name, value):
    """名称描述"""
    consoleLog(u'执行方法 %s 开始' % name)
    time.sleep(value)
    consoleLog(u'执行方法 %s 结束' % name)

# # loops = [2, 3]
# loops = (randrange(2, 5) for x in xrange(randrange(3, 7)))
# for loop in loops:
#     print loop
# print currentThread().name
time.clock()
time.clock()
if __name__ == '__main__':
    for i in range(5):
        Thread(target=test, args=(i, i)).start()

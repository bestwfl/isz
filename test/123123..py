# -*- coding:utf8 -*-

from common.base import log, consoleLog, Base
from common import sqlbase
import time


class ResInfo(object):
     def __init__(self, res_id):
         self.res_id = res_id
         pass

class Res(object):

    @staticmethod
    def createRes(res_name):
        url = ''
        data = {"res_name" : res_name}
        res_id = None
        # return ResInfo(res_id)


if __name__ == '__main__':
    res = Res.createRes('res_name')
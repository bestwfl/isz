# -*- coding:utf8 -*-

from common.base import log, consoleLog, Base
from common import sqlbase
import time
from common.interface_wfl import myRequest, consoleLog


class DingUser:
    def __init__(self):
        self._id = None
        self._name = None
        self._dep_id = None
        self._dep_name = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def dep_id(self):
        return self._dep_id

    @dep_id.setter
    def dep_id(self, value):
        self._dep_id = value

    @property
    def dep_name(self):
        return self._dep_name

    @dep_name.setter
    def dep_name(self, value):
        self._dep_name = value

class DingDing:
    def __init__(self):
        self.corpid = 'ding31f70bb0d79aa578'
        self.corpsecret = 'Wbd3Ufh-0D0WWFyVRjbReXHEm9IWkoTgVjL15QiMCbig6rWhiQ1m5R-s4S9t5daQ'
        self.access_token = '2735ae8b3bde3f47930580b6262b1555'

    def getToken(self):
        """名称描述"""
        url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (self.corpid, self.corpsecret)
        self.access_token = myRequest(url, method='get', needCookie=False)['access_token']

    def getAllDep(self):
        """名称描述"""
        url = 'https://oapi.dingtalk.com/department/list?access_token=%s' % self.access_token
        return myRequest(url, method='get', needCookie=False)

    def getUserByDepId(self, dep_id):
        """名称描述"""
        url = 'https://oapi.dingtalk.com/user/list?department_id=%s&access_token=%s' % (dep_id, self.access_token)
        return myRequest(url, method='get', needCookie=False)


if __name__ == '__main__':
    d = DingDing()
    print d.getAllDep()

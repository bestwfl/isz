# -*- coding:utf8 -*-
import requests
from flask import json

from common.base import consoleLog, set_conf

headers = {
    'content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
}
host = 'http://isz.ishangzu.com/'

def myRequest(url, cookie, data=None, needCookie=True, method='post', returnValue=False, ):
    interfaceURL = host + url
    if method == 'get':
        if needCookie:
            request = requests.get(url, cookie=cookie)
        else:
            request = requests.get(url)
    if method == 'post':
        if needCookie:
            request = requests.post(interfaceURL, data=json.dumps(data), headers=headers, cookies=cookie)
        else:
            request = requests.post(interfaceURL, data=json.dumps(data), headers=headers)
    result = json.loads(request.text)
    if request.status_code is not 200 or result['code'] is not 0:
        msg = result['msg'].encode('utf-8')
        consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (interfaceURL, data, msg.decode('utf-8')), 'w')
        return False if not returnValue else msg
    else:
        return result

class MyRequest(object):

    def __init__(self, user, password):
        url = 'http://isz.ishangzu.com/isz_base/LoginController/login.action'
        data = {"user_phone": user, "user_pwd": password, "auth_code": "",
                "LechuuPlatform": "LECHUU_CUSTOMER", "version": "1.0.0"}
        request = requests.post(url, data=json.dumps(data), headers=headers)
        self.cookies = {}
        result = json.loads(request.text)
        if result['msg'] == (u'登录成功'):
            self.cookies['ISZ_SESSIONID'] = request.cookies.get('ISZ_SESSIONID')
            self.cookies['CROSS_ISZ_SESSIONID'] = request.cookies.get('CROSS_ISZ_SESSIONID')
            print self.cookies
            set_conf('cookieInfo', cookies=self.cookies)
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'登录失败！\n失败信息：%s' % (msg.decode('utf-8')), 'w')

user = '18815286582'
password = 'ceshi123456'
test = MyRequest(user, password)
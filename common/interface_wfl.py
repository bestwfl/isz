# -*- coding:utf8 -*-

import json
import traceback
import requests
import time
import os
import sys
from common.base import consoleLog, set_conf
from common.base import get_conf
from common.sqlbase import getsmsMtHis


def checckLogin(func):
    """检验登录状态"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        loginmsg = '请重新登陆'
        loginmsg2 = '请先登录系统'
        if loginmsg.encode('utf-8') in result or loginmsg2.encode('utf-8') in result:
            consoleLog('登录状态失效，尝试重新登录！')
            login()
            return func(*args, **kwargs)

    return wrapper


def testWithLogin(func):
    def wrapper(*args, **kwargs):
        login()
        try:
            return func(*args, **kwargs)
        except BaseException:
            traceback.print_exc()
            # consoleLog(e.message)
        finally:
            return

    return wrapper


def myRequest(url, data=None, needCookie=True, contentType='application/json', method='post', returnValue=False,
              shutdownFlag=False):
    headers = {
        'content-type': contentType,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    host = 'http://isz.ishangzu.com/'
    interfaceURL = host + url if not url.startswith('http') else url
    cookie = eval(get_conf('cookieInfo', 'cookies'))
    if url.find('http://decorationapp.ishangzu.com/') >= 0:
        cookie = eval(get_conf('cookieInfo', 'decorationapp_cookies'))
    request = None
    if method == 'get':
        if needCookie:
            request = requests.get(interfaceURL, cookies=cookie)
        else:
            request = requests.get(interfaceURL)
    if method == 'put':
        if needCookie:
            request = requests.put(interfaceURL, data=json.dumps(data), headers=headers, cookies=cookie)
        else:
            request = requests.put(interfaceURL, data=json.dumps(data), headers=headers)
    if method == 'post':
        if needCookie:
            request = requests.post(interfaceURL, data=json.dumps(data), headers=headers, cookies=cookie)
        else:
            request = requests.post(interfaceURL, data=json.dumps(data), headers=headers)
    try:
        result = json.loads(request.text)
    except ValueError:
        consoleLog(request)
        raise ValueError('ERROR')
    if 'code' not in result.keys():
        return result
    if request.status_code is not 200 or (result['code'] is not 0 and result['code'] is not 1):
        msg = result['msg'].encode('utf-8')
        loginmsg = u'请重新登陆'
        loginmsg2 = u'请先登录系统'
        if loginmsg.encode('utf-8') in msg or loginmsg2.encode('utf-8') in msg:
            consoleLog(u'登录状态失效，尝试重新登录！')
            login()
            return myRequest(url, data, needCookie, contentType, method, returnValue)
        consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (interfaceURL, data, msg.decode('utf-8')), 'w')
        if shutdownFlag:
            raise Exception('接口响应异常!')
        return False if not returnValue else msg
    else:
        return result


class Image(object):
    def __int__(self):
        self.id = None
        self.url = None
        self.src = None


def upLoadPhoto(url, filename, filepath=None, name='file'):
    """
    上传图片
    :param filepath:'C:\Users\user\Desktop\Image\\' 所在文件夹路径
    :param filename:文件名称
    :param name:请求文件类型
    :param url:上传地址
   """
    image = Image()
    if not filepath:
        filepath = sys.path[1] + '\img\\'
    filepath_l = filepath + filename
    if not os.path.exists(filepath_l):
        consoleLog('文件路径不存在，文件路径：%s' % filepath_l)
    try:
        filetype = {
            name: (str(filename).encode('utf-8'), open(str(filepath_l).encode('utf-8'), 'rb'), 'image/png'),
        }
        cookie = eval(get_conf('cookieInfo', 'cookies'))
        if url.find('http://decorationapp.ishangzu.com/') >= 0:
            cookie = eval(get_conf('cookieInfo', 'decorationapp_cookies'))
        request = requests.post(url=url, files=filetype, cookies=cookie)
        result = json.loads(request.text)
        if result['code'] is 200 or result['code'] == u'200' or result['code'] is 0:
            for key, value in result['obj'].items():
                if 'img_id' == key:
                    image.id = value
                if 'src' == key:
                    image.src = value
                    image.url = value
                if 'url' in key or 'photoUrl' == key:
                    image.url = value
                    image.src = value
        else:
            msg = result['msg'].encode('utf-8')
            if '登陆' in msg:
                if url.find('http://decorationapp.ishangzu.com/') >= 0:
                    Decoration.decorationAppLogin()
                login()
                return upLoadPhoto(url, filename, filepath, name)
            else:
                consoleLog(u'上传文件接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s\n返回默认图片' % (url, filetype, msg.decode('utf-8')), 'w')
                image.url = get_conf('img', 'url')
                image.src = get_conf('img', 'src')
                image.id = get_conf('img', 'img_id')
    except Exception as e:
        consoleLog(e.args, 'e')
        image.url = get_conf('img', 'url')
        image.src = get_conf('img', 'src')
        image.id = get_conf('img', 'img_id')
    return image


def login(user=get_conf('sysUser', 'userPhone'), pwd=get_conf('sysUser', 'pwd')):
    needClient = None
    # 默认登录不使用客户端，如果报错，则赋值给needClient为True，然后调用客户端的登录接口进行校验
    url = 'http://isz.ishangzu.com/isz_base/LoginController/login.action'
    data = {
        'user_phone': user, 'user_pwd': pwd, 'auth_code': '', 'LechuuPlatform': 'LECHUU_CUSTOMER',
        'version': '1.0.0'
    }
    headers = {
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(response.text)
    if result['msg'] == u'登录成功' or result['msg'] == u'非生产环境,不做校验！':
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        set_conf('cookieInfo', cookies=cookies)
        consoleLog(u'登录成功!')
    elif u'密码错误' in result['msg']:
        msg = result['msg'].encode('utf-8')
        consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
        quit()
    else:
        needClient = True

    if needClient:
        from common.getAuthKey import getAuthKey
        auth_key = getAuthKey()
        # 检查授权
        url = 'isz_base/LoginAuthController/checkLoginAuth.action'
        data = {'auth_key': auth_key}
        result = myRequest(url, data, needCookie=False)
        msglogin = u'授权成功'
        if msglogin in result['msg']:
            auth_code = result['obj']['authList'][0]['auth_code']
            authTag = result['obj']['authTag']
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise BaseException(u'客户端登录第一步：检查授权失败')

        # 检查用户名密码
        url = 'isz_base/LoginController/checkUserPassWord.action'
        data = {
            'auth_code': auth_key,
            'authTag': authTag,
            'user_phone': user, 'user_pwd': pwd
        }
        result = myRequest(url, data, needCookie=False)
        if u'用户名密码正确' not in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise BaseException(u'客户端登录第二步：检查用户名密码失败')

        # 获取短信验证码
        url = 'isz_base/LoginController/getVerificationCode.action'
        data = {
            'authTag': authTag,
            'mobile': user
        }
        result = myRequest(url, data, needCookie=False)
        msg1 = u'验证码发送过于频繁'
        if result['msg'] != 'ok' and msg1 not in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise BaseException(u'客户端登录第三步：获取短信验证码失败')

        # 验证码登录
        url = 'isz_base/LoginController/checkVerificationCode.action'
        data = {
            'auth_code': auth_key,
            'authTag': authTag,
            'user_phone': user,
            'user_pwd': pwd,
            'verificationCode': '0451'
        }
        if get_conf('testCondition', 'test') == 'online':  # 线上从MANGO中取短信验证码登录
            time.sleep(2)  # 线上短信可能延迟
            sms_code = getsmsMtHis(user)  # mangoDB中取短信记录
            data['verificationCode'] = sms_code
        # 判断是否是开发部，然后决定验证码是默认的0451还是从数据库查最新收到的
        # if not myRequest(url, data, needCookie=False):
        #     dep_name = u'技术开发中心'
        #     sql = "select * from sys_department_flat where dept_id=(SELECT dep_id from sys_department where dep_name = '%s') and child_id=(" \
        #           "SELECT dep_id from sys_user where user_phone = '%s' and user_status = 'INCUMBENCY')" % (dep_name, user)
        # if sqlbase.get_count(sql) == 0 or get_conf('testCondition', 'test') == 'online':
        #     # content = sqlbase.serach("SELECT content from sms_mt_his where destPhone = '%s' ORDER BY create_time desc limit 1" % user)[0]
        #     # sms_code = re.findall('验证码：(.*?)，', content.encode('utf-8'))[0]
        #     time.sleep(2)  # 线上短信可能延迟
        #     sms_code = getsmsMtHis(user)  # mangoDB中取短信记录
        #     data['verificationCode'] = sms_code
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }
        url = 'http://isz.ishangzu.com/isz_base/LoginController/checkVerificationCode.action'
        response = requests.post(url, data=json.dumps(data), headers=headers)
        result = json.loads(response.text)
        if result['msg'] == 'ok':
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            set_conf('cookieInfo', cookies=cookies)
            consoleLog(u'登录成功')
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise BaseException(u'客户端登录第四步：验证码登录失败')


def delNull(data):
    """删除字典中为null的值"""

    def typeDict(data):
        for x, y in data.items():
            if y is None or y == '':
                del data[x]
            elif type(y) is list:
                typeList(data[x])
            elif type(y) is dict:
                typeDict(data[x])

    def typeList(data):
        for x, y in enumerate(data):
            if type(y) is dict:
                typeDict(data[x])
            if y is None:
                del data[x]

    typeDict(data) if type(data) is dict else typeList(data)
    return data


if __name__ == '__main__':
    uploadPhotoURL = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/uploadImageFile'  # 委托合同上传图片地址
    idCardPhotos = upLoadPhoto(url=uploadPhotoURL, filename='idCardPhotos.png',
                               filepath=r"C:\Users\user\Desktop\Image\\")
    print idCardPhotos

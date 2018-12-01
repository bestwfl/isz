# -*- coding:utf8 -*-
import random
from collections import OrderedDict

import time
from pymongo import MongoClient
import requests
from requests_toolbelt import MultipartEncoder

from isz.houseContract import HouseContract
from common.base import get_conf
from common.dict import User
from common.interface_wfl import login, upLoadPhoto
from common.sqlbase import getsmsMtHis
import os
from poster.encode import multipart_encode

# @testWithLogin
def decorationNew():
    print getsmsMtHis(18815286582)

def mangodb():
    # mango_uri = "mongodb://%s:%s@%s:%s/%s" % ('root', 'Ishangzu_mongodb', '192.168.0.200', '27020', 'sms' )
    conn = MongoClient('192.168.0.200', 27020)
    conn = MongoClient('mongodb://root:Ishangzu_mongodb@192.168.0.200:27020/')
    db = conn.sms
    table = db.smsMtHis
    row = table.find({'destPhone': '18815286582'}).sort([{"create_time", -1}])
    for i in row:
        print i['content']

def test3():
    for i, j in range(3),range(3):
        print i,j



if __name__ == '__main__':
    login()
    url = 'http://decorate.ishangzu.com/isz_decoration/DecorationFileController/uploadPhoto'
    filename = 'Two.png'
    filepath = 'C:\Users\user\Desktop\Image\\'
    # file = {
    #         'file': (str(filename).encode('utf-8'), open(str(filepath).encode('utf-8'), 'rb'), 'image/png'),
    #         }
    # cookie = eval(get_conf('cookieInfo', 'cookies'))
    # result = requests.post(url=url, files=file, cookies=cookie)
    img = upLoadPhoto(url, filepath=filepath, filename=filename)

    time.sleep(1)
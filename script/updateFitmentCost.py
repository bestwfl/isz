# -*- coding:utf8 -*-
import time

from common.base import consoleLog
from common.interface_wfl import myRequest

project_ids = ['822', '848', '847', '878', '870', '871', '943', '1027', '1117']
url_base = 'http://decorate.ishangzu.com/isz_decoration/CompleteCostCheckController/sendDummyMsg/'
i = 0
for project_id in project_ids:
    i = i + 1
    url = url_base + project_id
    myRequest(url, method='get', needCookie=True)
    consoleLog(i)
    time.sleep(1)

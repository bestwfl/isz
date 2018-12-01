# -*- coding:utf8 -*-

from common.base import log, consoleLog, Base
import time
from common.interface_wfl import myRequest
from common.mySql import Mysql


def test():
    """名称描述"""
    searchSQl = "select verify_id from isz_erp_finance.house_charge_account_verify where account_identify='UNKNOW' and deleted=0"
    result = Mysql().getAll(searchSQl)
    url = "http://rsm.ishangzu.com/isz_balanceofaccount/HouseChargeAccountController/account/officialAddress/{}"
    for index, item in enumerate(result):
        try:
            newUrl = url.format(item)
            myRequest(newUrl, method='put')
            consoleLog("{}:verify_id:{}已调浦发接口查询".format(index+1, item))
            time.sleep(1)
        except Exception as e:
            consoleLog(e.message)

if __name__ == '__main__':
    test()

# -*- coding:utf8 -*-

# Author : Zhong Ling Long
# Create on : 2018年2月11日09:34:26

"""
该模块是财务生成付款单的定时器
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *

def add_pay_timer(payable_date):
    """
    付款单定时器
    :param payable_date:付款日期
    :return:
    """
    if re_search(r"20[0-9]+[0-9]+-[0-1]+[0-9]+-[0-3]+[0-9]+",payable_date) == None or len(payable_date) != 10:
        return "日期输入格式不对！参考：2018-01-01"
    url = "http://fms.ishangzu.com/isz_balanceofaccount/PayManageController/testCreatePayment"
    data = {"payable_date":payable_date}

    return myRequest(url,str(data),Value=True)

host_set("test")
get_cookie()

print add_pay_timer("2018-02-15")
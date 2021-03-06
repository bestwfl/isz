# -*- coding:utf8 -*-

from common.base import log, consoleLog, Base
from common import sqlbase
import time

from isz.decoration import Decoration

if __name__ == '__main__':
    contractNum = u'FF808081672B4157016730E031960740'
    decoration = Decoration(contractNum)
    decoration.newPlaceOrder()  # 下单
    # decoration.placeOrder()  # 下单
    decoration.dispatchOrder()  # 派单
    decoration.appAcceptOrder()  # 接单
    # decoration.acceptOrder()  # 接单
    # decoration.survey(is_need_waterproofing='Y')  # 勘测
    # decoration.projectOrder()  # 项目计划
    # decoration.configList()  # 物品清单
    # decoration.stuffList()  # 装修清单
    # decoration.hideAndStufCheck()  # 施工中
    # decoration.projectCheck()  # 项目验收
    # decoration.indoorImg()  # 室内图
    # decoration.delivery()  # 竣工

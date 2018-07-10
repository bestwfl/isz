# -*- coding:utf8 -*-

import time
from threading import Thread

import threadpool

from common import sqlbase
from common.base import get_randomString, consoleLog
from common.datetimes import today, addMonths, addDays
from common.interface_wfl import login
from isz.house import House


def createHouseContract(houseInfo):
    """新签委托合同"""
    house = House(houseInfo[0])
    consoleLog('签约房源：%s, %s, %s' % (house.house_id, house.house_code, house.property_name))
    # 委托合同参数
    contract_num_sign = u'WFL工程1.5'  # 合同标识
    contract_num = '%s-%s%s' % (contract_num_sign, time.strftime('%m%d%H%M'), get_randomString(2))
    apartment_type = 'BRAND'
    entrust_type = 'ENTIRE'
    sign_date = today()
    owner_sign_date = today()
    fitment_start_date = addDays(1, sign_date)
    fitment_end_date = addMonths(1, sign_date)
    entrust_start_date = addDays(1, fitment_end_date)
    entrust_year = 3
    rent = 1234.34
    parking = 123
    # try:
    contract = house.createHouseContract(contract_num=contract_num, apartment_type=apartment_type,
                                         entrust_type=entrust_type, sign_date=sign_date,
                                         owner_sign_date=owner_sign_date, fitment_start_date=fitment_start_date, fitment_end_date=fitment_end_date,
                                         entrust_start_date=entrust_start_date, entrust_year=entrust_year, rent=rent,
                                         parking=parking)
    # contract.audit('fushen')
    # decoration = Decoration(contract.house_contract_id)
    # decoration.fitment()
    # time.sleep(3)
    # apartment = Apartment(houseInfo[1])
    # apartment.confirmPrice(2000)
    # except:
    #     # consoleLog()
    #     consoleLog(u'委托合同创建失败，房源编号：%s' % houseInfo[1])
    #     pass


if __name__ == '__main__':
    houseSql = "SELECT a.house_id, a.house_code,a.property_name FROM house a WHERE a.deleted=0 AND a.city_code LIKE '3301%'  " \
               "AND NOT EXISTS(SELECT * FROM house_contract b WHERE b.house_id=a.house_id ) " \
               "AND EXISTS(SELECT * FROM residential_building rb WHERE rb.building_id=a.building_id AND deleted=0) " \
               "AND EXISTS(SELECT * FROM residential c WHERE a.residential_id=c.residential_id) " \
               "AND EXISTS(SELECT * FROM house_rent hr WHERE hr.house_id=a.house_id AND house_status='WAITING_RENT') " \
               "ORDER BY rand() LIMIT 1"
    houseInfos = sqlbase.serach(houseSql, oneCount=False)
    consoleLog('查询结束')
    login()
    pool = threadpool.ThreadPool(2)
    requests = threadpool.makeRequests(createHouseContract, houseInfos)
    [pool.putRequest(req) for req in requests]
    pool.wait()

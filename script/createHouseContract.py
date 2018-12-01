# -*- coding:utf8 -*-

import time

import threadpool

from common import sqlbase
from common.base import get_randomString, consoleLog
from common.datetimes import today, addMonths, addDays
from common.interface_wfl import login
from isz.decoration import Decoration
from isz.house import House
import traceback

def trycatch(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            consoleLog(traceback.format_exc())
            consoleLog(e.args, 'e')
    return wrapper

@trycatch
def createHouseContract(houseInfo):
    """新签委托合同"""
    house = House(houseInfo[0])
    consoleLog('签约房源：%s, %s, %s' % (house.house_id, house.house_code, house.property_name))
    # 委托合同参数
    contract_num_sign = u'WFL-2.0'  # 合同标识
    apartment_type = 'BRAND'
    entrust_type = 'ENTIRE'
    contract_num = '%s%s%s%s-%s' % (contract_num_sign, apartment_type[0], entrust_type[0], time.strftime('%m%d%H%M'), get_randomString(2))
    sign_date = addMonths(-2, today())
    # sign_date = addDays(-20, today())
    owner_sign_date = addDays(1, sign_date)
    fitment_start_date = addDays(3, sign_date)
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
    decoration = Decoration(contract.house_contract_id)
    # decoration.fitment()
    # apartment = Apartment(houseInfo[1])
    # apartment.confirmPrice(2000)



if __name__ == '__main__':
    houseSql = "SELECT a.house_id, a.house_code,a.property_name FROM isz_erp.house a WHERE a.deleted=0 AND a.city_code LIKE '3301%'  " \
               "AND NOT EXISTS(SELECT * FROM isz_erp.house_contract b WHERE b.house_id=a.house_id ) AND a.residential_id<>'FF80808164913C65016497E9F3E7001C'" \
               "AND EXISTS(SELECT * FROM isz_erp.residential_building rb WHERE rb.building_id=a.building_id AND deleted=0) " \
               "AND EXISTS(SELECT * FROM isz_erp.residential c WHERE a.residential_id=c.residential_id) " \
               "AND EXISTS(SELECT * FROM isz_erp.house_rent hr WHERE hr.house_id=a.house_id AND house_status='WAITING_RENT')" \
               "ORDER BY rand() LIMIT 1"
    # houseSql = "SELECT a.house_id, a.house_code,a.property_name FROM house a where a.house_code='HZXS1705260574'"
    houseInfos = sqlbase.serach(houseSql, oneCount=False)
    print houseInfos
    # createHouseContract(houseInfos[0])
    consoleLog('业主房源查询结束')
    login()
    pool = threadpool.ThreadPool(4)
    requests = threadpool.makeRequests(createHouseContract, houseInfos)
    [pool.putRequest(req) for req in requests]
    pool.wait()


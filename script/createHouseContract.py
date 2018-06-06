# -*- coding:utf8 -*-

import time
from isz.apartment import Apartment
from isz.decoration import Decoration
from isz.house import House
from common import sqlbase
from common.base import get_randomString, consoleLog
from common.datetimes import today, addMonths
from threading import Thread

def createHouseContract(houseInfo):
        """新签委托合同"""
        house = House(houseInfo[0])
        consoleLog(u'签约房源：%s, %s, %s' % (house.house_id, house.house_code, house.property_name))
        # 委托合同参数
        contract_num_sign = u'WFL工程1.4'  # 合同标识
        contract_num = '%s-%s%s' % (contract_num_sign, time.strftime('%m%d%H%M'), get_randomString(2))
        apartment_type = 'BRAND'
        entrust_type = 'ENTIRE'
        sign_date = addMonths(-12, today())
        owner_sign_date = addMonths(-12, today())
        entrust_start_date = addMonths(-12, today())
        entrust_year = 3
        rent = 1234.34
        parking = 123
        # try:
        contract = house.createHouseContract(contract_num=contract_num, apartment_type=apartment_type, entrust_type=entrust_type, sign_date=sign_date, owner_sign_date=owner_sign_date,
                                                entrust_start_date=entrust_start_date, entrust_year=entrust_year, rent=rent, parking=parking)
        contract.audit('fushen')
        decoration = Decoration(contract.contract_id)
        decoration.fitment()
            # time.sleep(3)
            # apartment = Apartment(houseInfo[1])
            # apartment.confirmPrice(2000)
        # except:
        #     # consoleLog()
        #     consoleLog(u'委托合同创建失败，房源编号：%s' % houseInfo[1])
        #     pass

if __name__ == '__main__':
    houseSql = "SELECT a.house_id, a.house_code,a.property_name FROM house a WHERE a.deleted=0 AND a.city_code LIKE '330%'  " \
               "AND NOT EXISTS(SELECT * FROM house_contract b WHERE b.house_id=a.house_id ) " \
               "AND EXISTS(select * from residential_building rb where rb.building_id=a.building_id and deleted=0) " \
               "AND EXISTS(select * from residential c where a.residential_id=c.residential_id) "\
               "AND EXISTS(select * from house_rent hr where hr.house_id=a.house_id and house_status='WAITING_RENT') " \
               "ORDER BY rand() LIMIT 1"
    houseInfos = sqlbase.serach(houseSql, oneCount=False)
    for houseInfo in houseInfos:
        Thread(target=createHouseContract, args=(houseInfo,), name='addHouseContract on house:%s' % houseInfo[1]).start()
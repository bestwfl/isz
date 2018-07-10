# -*- coding:utf8 -*-
import time
import datetime
from isz.apartment import Apartment
from common import sqlbase
from common.base import consoleLog, get_conf
from common.interface_wfl import myRequest


class Repair(object):
    """报修相关
    :param apartmentIdOrNum:房源编号或者ID
    """

    def __init__(self, apartmentIdOrNum):
        apartmentInfo = sqlbase.serach(
            "select apartment_id,apartment_code,apartment_type,rent_status,rent_type,house_id,room_id from apartment where (apartment_id='%s' or apartment_code='%s') "
            "and is_active='Y' and deleted=0" % (apartmentIdOrNum, apartmentIdOrNum))
        self.__apartment_id = apartmentInfo[0]
        self.__apartment_code = apartmentInfo[1]
        self.__apartment_type = apartmentInfo[2]
        self.__rent_status = apartmentInfo[3]
        self.__rent_type = apartmentInfo[4]
        self.__house_id = apartmentInfo[5]
        self.__room_id = apartmentInfo[6]
        self.__house_property = 'INRENT'  # 房源属性	VACANCY：空置，INRENT:在租
        # 出租相关
        apartmentContractInfo = sqlbase.serach(
            "select a.contract_id,a.contract_num,a.sign_name,a.person_id,a.sign_phone from apartment_contract a inner join apartment_contract_relation  b on a.contract_id=b.contract_id "
            "inner join apartment c on c.apartment_id=b.apartment_id where c.apartment_id='%s' and a.deleted=0 and a.is_active='Y'" % self.__apartment_id,
            nullLog=False)
        if not apartmentContractInfo:
            consoleLog(u'房源 %s 下无有效出租合同' % self.__apartment_code)
            self.__house_property = 'VACANCY'
        self.__apartment_contract_id = apartmentContractInfo[0] if apartmentContractInfo else None
        self.__apartment_contract_num = apartmentContractInfo[1] if apartmentContractInfo else None
        self.__customer_name = apartmentContractInfo[2] if apartmentContractInfo else None
        self.__customer_id = apartmentContractInfo[3] if apartmentContractInfo else None
        self.__customer_phone = apartmentContractInfo[4] if apartmentContractInfo else None
        # 委托相关
        houseContractInfo = sqlbase.serach(
            "select a.contract_id, a.contract_num,b.property_name from house_contract a inner join house b on a.house_id=b.house_id where a.house_id='%s' and a.deleted=0 "
            "and a.is_active='Y'" % self.__house_id)
        self.__house_contract_id = houseContractInfo[0]
        self.__house_contract_num = houseContractInfo[1]
        self.__house_property_name = houseContractInfo[2]

    def createRepair(self):
        """新增报修订单"""
        url = 'http://rsm.ishangzu.com/isz_repair/RepairsController/repairsOrder'
        data = {
            "house_id": self.__house_id,
            "house_contract_id": self.__house_contract_id,
            "apartment_contract_id": self.__apartment_contract_id,
            "apartment_contract_num": self.__apartment_contract_num,
            "apartment_num": self.__apartment_code,
            "apartment_type": self.__apartment_type,
            "rent_status": self.__rent_status,
            "rent_type": self.__rent_type,
            "house_address": '%s%s' % (self.__house_property_name, Apartment.roomName(self.__room_id)),
            "apartment_id": self.__apartment_id,
            "customer_id": self.__customer_id,
            "customer_name": self.__customer_name,
            "house_property": self.__house_property,
            "room_id": self.__room_id,
            "linkman_name": self.__customer_name if self.__customer_name else u'维修联系人',
            "linkman_phone": self.__customer_phone if self.__customer_phone else '13600000000',
            "repairs_area": "WOSHI",
            "repairs_type": "WOSHIZHUTI",
            "repairs_project": "WOSHIZHUTIDIAODING",
            "content": "破损",
            "supplier_repair": "ONLINEUP",  # 申请报修方式
            "repair_status": "N",
            "repairs_source": "ERP",
            "invited_date": (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
            "repairsLableRelation": [
                {
                    "label_id": "cb5d6e75ede111e6ae531866daf07138",
                    "label_type": "ANGUANLOUSHUI"
                }, {
                    "label_id": "cb57cb5aede111e6ae531866daf07138",
                    "label_type": "POSUN"
                }, {
                    "label_id": "cb522df3ede111e6ae531866daf07138",
                    "label_type": "TUOLUO"
                }
            ],
            "repairsCost": {
                "supplier_name": "",
                "supplier_person_name": "",
                "supplier_person_phone": "",
                "total_cost": "",
                "finish_time": "",
                "remark": "",
                "repairsCostDetails": [{
                    "bears_money": "",
                    "bears_name": "",
                    "bears_type": "",
                    "buckle_price_date": "1971-01-01 00:00:00",
                    "contract_id": "",
                    "contract_num": "",
                    "cost_type": "",
                    "housing_uid": "",
                    "housing_name": "",
                    "housing_money": "",
                    "customers_uid": "",
                    "customers_name": "",
                    "customers_money": "",
                    "buckle_money_type": "",
                    "isCompany": False
                }]
            },
            "repairsAttachments": [{
                "img_id": "FF80808162FB8AF70162FC3396F209A7",
                "img_url": "http://file.ishangzu.com/rsm/2018/4/25/17/9c014540-b3fe-4403-924e-d9b51c7862e3.png",
                "remark": "",
                "sort": ""
            }],
        }
        if myRequest(url, data):
            consoleLog(u'房源 %s 已添加报修' % self.__apartment_code)

    @staticmethod
    def orderNum(orderIdOrNum):
        order_id = sqlbase.serach(
            "select order_id from %s.repairs_order where (order_id='%s' or order_no='%s') and deleted=0" % (
                get_conf('db', 'rsm_db'), orderIdOrNum, orderIdOrNum))
        if order_id:
            return order_id[0]
        else:
            consoleLog(u'报修订单不存在！')

    @classmethod
    def placeOrder(cls, orderIdOrNum):
        order_id = cls.orderNum(orderIdOrNum)
        url = 'http://rsm.ishangzu.com/isz_repair/RepairsController/order/operation/FF8080816349F0F2016349FA50C10052'
        data = {
            "cooperation_type": "Y",  # 是否合作
            "supplier_id": "8A2152435BAF8739015BB39E767C007E",  # 供应商ID
            "order_status": "STAYDISTRIBUTION",  # 当前订单状态
            "remark": u'WFL下单',
            "order_id": order_id,
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        if myRequest(url, data):
            consoleLog(u'维修订单：%s已下单，供应商为')

    @staticmethod
    def cancel(order_id):
        url = 'http://rsm.ishangzu.com/isz_repair/RepairsController/order/%s/cancel' % order_id
        data = {
            'order_id': order_id,
            'reason': 'cancel by test',
            'update_time': '{}{}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), '.0')
        }
        if myRequest(url, data, method='put'):
            consoleLog(u'订单：%s 已取消' % order_id)


if __name__ == '__main__':
    apartments = sqlbase.serach("SELECT apartment_id,apartment_code FROM apartment WHERE is_active='Y' AND deleted=0 "
                                "AND rent_status<>'RENTED' AND rent_type='SHARE' AND city_code='330100' ORDER BY RAND() LIMIT 10",
                                oneCount=False)
    for apartment in apartments:
        consoleLog(u'房源编号：%s ID:%s' % (apartment[1], apartment[0]))
        repair = Repair(apartment[0])
        repair.createRepair()
        # Repair.cancel('FF808081636379B101636379C2960018')

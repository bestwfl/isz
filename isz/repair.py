# -*- coding:utf8 -*-
import datetime
import time
from common.base import consoleLog
from common.interface_wfl import myRequest, upLoadPhoto
from isz.infoClass import ApartmentInfo, RepairOrderInfo


class Repair(RepairOrderInfo):
    """报修相关
    :param apartmentIdOrNum:房源编号或者ID
    """
    _uploadPhotoURL = 'http://rsm.ishangzu.com/isz_repair/CommUploadPhotoController/uploadPhoto'

    def __init__(self, orderNumOrId):

        super(Repair, self).__init__(orderNumOrId)

    @classmethod
    def createRepair(cls, apartmentCodeOrId):
        """新增报修订单
        :param apartmentCodeOrId 房源Code或者Id
        """
        apartment = ApartmentInfo(apartmentCodeOrId)
        apartment_contract = apartment.apartment_contract
        if apartment_contract:
            apartment_contract_id = apartment_contract.apartment_contract_id
            apartment_contract_num = apartment_contract.apartment_contract_num
            customer = apartment_contract.custmoer_person()
            customer_id = customer.person_id
            customer_name = customer.customer_name
            customer_phone = customer.phone
        else:
            apartment_contract_id = None
            apartment_contract_num = None
            customer_id = None
            customer_name = None
            customer_phone = None
        url = 'http://rsm.ishangzu.com/isz_repair/RepairsController/repairsOrder'
        img = upLoadPhoto(url=cls._uploadPhotoURL, filename='AddRepairs.png',
                          filepath=r"C:\Users\user\Desktop\Image\\")  # 报修图片上传
        data = {
            "house_id": apartment.house_id,
            "house_contract_id": apartment.house_contract_id,
            "apartment_contract_id": apartment_contract_id,
            "apartment_contract_num": apartment_contract_num,
            "apartment_num": apartment.apartment_code,
            "apartment_type": apartment.apartment_type,
            "rent_status": apartment.rent_status,
            "rent_type": apartment.rent_type,
            "house_address": apartment.apartment_property_name,
            "apartment_id": apartment.apartment_id,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "house_property": apartment.property_name,
            "room_id": apartment.room_id,
            "linkman_name": customer_name if customer_name else u'维修联系人',
            "linkman_phone": customer_phone if customer_phone else '13600000000',
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
                "img_id": img.id,
                "img_url": img.url,
                "remark": "",
                "sort": ""
            }],
        }
        if myRequest(url, data):
            consoleLog(u'房源 %s 已添加报修' % apartment.apartment_code)


    def placeOrder(self):
        url = 'http://rsm.ishangzu.com/isz_repair/RepairsController/order/operation/FF8080816349F0F2016349FA50C10052'
        data = {
            "cooperation_type": "Y",  # 是否合作
            "supplier_id": "8A2152435BAF8739015BB39E767C007E",  # 供应商ID
            "order_status": "STAYDISTRIBUTION",  # 当前订单状态
            "remark": u'WFL下单',
            "order_id": self.order_id,
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        if myRequest(url, data):
            consoleLog(u'维修订单：%s已下单，供应商为')


    def cancel(self):
        url = 'http://rsm.ishangzu.com/isz_repair/RepairsController/order/%s/cancel' % self.order_id
        data = {
            'order_id': self.order_id,
            'reason': 'cancel by test',
            'update_time': '{}{}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), '.0')
        }
        if myRequest(url, data, method='put'):
            consoleLog(u'订单：%s 已取消' % self.order_no)


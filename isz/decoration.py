# -*- coding:utf8 -*-

import time

from sqlalchemy import true

from isz.houseContract import HouseContract
from common import sqlbase
from common.base import consoleLog, get_conf, set_conf
from common.datetimes import addDays, today
from common.interface_wfl import myRequest, upLoadPhoto
from common.dict import User
from common.mySql import Mysql
import requests
import json


class Decoration(object):
    """装修工程"""
    uploadPhotoURL = 'http://decorate.ishangzu.com/isz_decoration/DecorationFileController/uploadPhoto'  # 装修工程上传图片地址
    mysql = Mysql()

    def __init__(self, contractIdOrNum):
        self.project_id = None
        nullLog = False
        for i in range(15):
            project = self.mysql.getOne(
                "select project_id,b.contract_num,b.sign_uid,a.info_id,b.address,b.pristine_family from isz_decoration.new_decoration_project a inner join isz_decoration.decoration_house_info b "
                "on a.info_id=b.info_id  where b.deleted=0 and (b.contract_num='%s' or b.contract_id='%s')" % (
                    contractIdOrNum, contractIdOrNum), nullLog=nullLog)
            if project:
                self.project_id = project[0]
                self.contract_num = project[1]
                self.sign_uid = project[2]
                self.info_id = project[3]
                self.address = project[4]
                self.pristine_family = project[5]
                self.timestamp = None
                self.task_Id = self.mysql.getOne(
                    "SELECT art.ID_ FROM isz_activiti.act_ru_execution are LEFT JOIN isz_activiti.act_ru_task art ON are.`PROC_INST_ID_` = art.`PROC_INST_ID_` WHERE are.`BUSINESS_KEY_`='{}'".format(
                        self.project_id))[0]
                break
            elif i < 14:
                time.sleep(1)
                if i == 13:
                    nullLog = True
            else:
                raise BaseException('the house_contract does not exist decoration order, contract：%s' % contractIdOrNum)

    @property
    def predict_survey_date(self):
        return self.mysql.getOne(
            "select left(predict_survey_date,10) from isz_decoration.new_decoration_project where project_id='%s'" % self.project_id)[
            0]

    @property
    def taskId(self):
        return self.mysql.getOne(
            "select art.ID_ from isz_activiti.act_ru_execution are LEFT JOIN isz_activiti.act_ru_task art on are.PROC_INST_ID_ = art.PROC_INST_ID_ where are.BUSINESS_KEY_='%s'"
            % self.project_id)[0]

    # 下单
    def placeOrder(self):
        consoleLog(u'--------开始工程管理--------')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/placeOrder'
        data = {
            'place_order_dep': User.DID,
            'place_order_reason': u'测试',
            'place_order_uid': User.UID,
            'place_order_uname': User.NAME,
            'place_order_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'predict_survey_date': '%s 09:00' % addDays(1),
            'project_id': self.project_id
        }
        result = myRequest(url, data)
        if result:
            # consoleLog(u'下单完成')
            return

    def newPlaceOrder(self):
        """2.0下单"""
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/placeOrder'
        data = {
            'place_order_dep': User.DID,
            'place_order_dep_name': User.D_NAME,
            'place_order_reason': "新收配置订单",
            'place_order_uid': User.UID,
            'place_order_uname': User.NAME,
            'place_order_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'predict_survey_date': "",
            'project_id': self.project_id
        }
        result = myRequest(url, data)
        if result:
            return

    # 派单
    def dispatchOrder(self):
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/dispatchOrder'
        data = {
            # 'construct_uid': '1610',
            # 'construct_uid': '8AB398CA550C536B01550C536BCC0000',
            # 'construct_uname': u'test_吴俊',

            'construct_uid': 'FF808081666B4CE2016671193ACC00A7',
            'construct_uname': 'test_王方龙_01',
            'dispach_remark': '测试',

            'project_id': self.project_id,
            'supplier_id': '8A2152435FBAEFC3015FBAEFC3000000',
            'supplier_uid': '8AB398CA5FBAF072015FBB26338A0002',
            'predict_survey_date': '%s 09:00' % addDays(1),
            'supplier_name': '测试专用硬装供应商',
            'supplier_uname': '测试专用硬装员工'

            # 'supplier_uid': 'FF808081670708030167070803CA0000',
            # 'supplier_uname': u'test_solxnp'
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'派单完成')
        else:
            raise Exception('派单失败!')

    def newDispatchOrder(self):
        """派单2.0"""
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/dispatchOrder'
        if get_conf('testCondition', 'test') == 'test':
            data = {
                "construct_uid": "FF808081666B4CE2016671193ACC00A7",
                "construct_uname": "test_王方龙_01",
                "dispach_remark": "测试派单",
                "supplier_id": "8A2152435FBAEFC3015FBAEFC3000000",
                "supplier_uid": "8AB398CA5FBAF072015FBB26338A0002",
                "supplier_name": "测试专用硬装供应商",
                "supplier_uname": "测试专用硬装员工",
                "project_id": self.project_id
            }
        elif get_conf('testCondition', 'test') == 'mock':
            data = {
                "construct_uid": "FF80808163AB43EE0163B4CED5BD041F",
                "construct_uname": "mock_王方龙_03",
                "dispach_remark": "测试派单",
                "project_id": self.project_id,
                "supplier_id": "8A2152435FBAEFC3015FBAEFC3000000",
                "supplier_uid": "FF8080816735879301673A6C46520042",
                "supplier_name": "测试专用硬装供应商",
                "supplier_uname": "WFL项目经理"
            }
        result = myRequest(url, data)
        if result:
            consoleLog('派单完成')
        else:
            raise Exception('派单失败!')

    # 接单2.0
    def newAcceptOrder(self):
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/acceptOrder'
        data = {"project_id": self.project_id, "predict_survey_date": today(), "remark": ""}
        result = myRequest(url, data)
        if result:
            consoleLog(u'接单完成')
            return

    # 接单
    def acceptOrder(self):
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/acceptOrder'
        data = {
            'project_id': self.project_id,
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'接单完成')
            return

    # 量房
    def survey(self, is_need_waterproofing='Y'):

        # 测量
        def score():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/score'
            data = {
                'grade': '20',
                'project_id': self.project_id,
                'reform_way_fact': 'REFORM',
                'score_remark': '',
                'attachments': [{
                    'attach_type': 'TOILET',
                    'imgs': [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 0,
                        'type': 'TOILET'
                    }]
                }, {
                    'attach_type': 'KITCHEN',
                    'imgs': [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 1,
                        'type': 'KITCHEN'
                    }]
                }, {
                    'attach_type': 'LIVING_ROOM',
                    'imgs': [{
                        'url': 'http://image.ishangzu.com/rsm/2018/3/7/17/624f6b13-298c-4a17-be49-efa3dc6af026.jpg',
                        'img_id': 'FF80808161FFCB3A0161FFCB3A700002',
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 2,
                        'type': 'LIVING_ROOM'
                    }]
                }, {
                    'attach_type': 'ROOM',
                    'imgs': [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 3,
                        'type': 'ROOM'
                    }]
                }, {
                    'attach_type': 'OTHER',
                    'imgs': [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 4,
                        'type': 'OTHER'
                    }]
                }]
            }
            for attachment in data['attachments']:
                IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % attachment['attach_type'],
                                  filepath=r"C:\Users\user\Desktop\Image\\")
                attachment['imgs'][0]['url'] = IMG.url
                attachment['imgs'][0]['img_id'] = IMG.id
            result = myRequest(url, data)
            if result:
                # consoleLog(u'测量完成')
                return

        # 物业交割
        def profee():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/profee'
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='PROPERTY_DELIVERY_ORDER.png',
                              filepath=r"C:\Users\user\Desktop\Image\\")
            data = {
                'air_switch': '',
                'door_card': '',
                'door_key': '',
                'electricity_card': '',
                'electricity_meter_num': '',
                'electricity_meter_remain': '',
                'gas_card': '',
                'gas_meter_num': '',
                'gas_meter_remain': '',
                'project_id': str(self.project_id),
                'water_card': '',
                'water_card_remain': '',
                'water_meter_num': '',
                'attachments': [{
                    'attach_type': 'PROPERTY_DELIVERY_ORDER',
                    'imgs': [{
                        "url": IMG.url,
                        "img_id": IMG.id,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 0,
                        'type': ''
                    }]
                }],
                'resource': 'SURVEY'
            }
            result = myRequest(url, data)
            if result:
                # consoleLog(u'物业交割完成')
                return

        # 闭水
        def closed():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/closed'
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='SCENE.png')
            data = {
                'air_switch': None,
                'attachments': [{
                    'attach_type': 'SCENE',
                    'imgs': [{
                        "url": IMG.url,
                        "img_id": IMG.id,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 0,
                        'type': ''
                    }]
                }],
                'check_remark': None,
                'closed_water_test_result': 'Y',
                'is_need_waterproofing': is_need_waterproofing,
                'curOneLevelNode': None,
                'curTwoLevelNode': None,
                'door_card': None,
                'door_key': None,
                'electricity_card': None,
                'electricity_meter_num': None,
                'electricity_meter_remain': None,
                'gas_card': None,
                'gas_meter_num': None,
                'gas_meter_remain': None,
                'grade': 20,
                'landlordGoods': None,
                'project_id': self.project_id,
                'reform_way_fact': None,
                'reform_way_fact_name': '',
                'remark': '测试',
                'score_remark': None,
                'water_card': None,
                'water_card_remain': None,
                'water_meter_num': None
            }
            result = myRequest(url, data)
            if result:
                # consoleLog(u'闭水完成')
                return

        score()
        profee()
        closed()
        consoleLog(u'量房完成')

    # 项目计划
    def projectOrder(self):
        # projectInfo = sqlbase.serach(
        projectInfo = Mysql().getOne(
            "select b.info_id,a.project_no,b.entrust_type,b.build_area from isz_decoration.new_decoration_project a "
            "inner join isz_decoration.decoration_house_info b on a.info_id=b.info_id "
            "and a.project_id='%s' where b.deleted=0 " % self.project_id)
        url = 'http://decorate.ishangzu.com/isz_decoration/decoHouseInfoController/saveOrUpdateApartment/saveApartment/projectOrder'
        img = upLoadPhoto(url=self.uploadPhotoURL, filename='LAYOUT.png',
                          filepath=r"C:\Users\user\Desktop\Image\\")  # 户型图上传
        data = {
            'build_area': projectInfo[3],
            'reform_way_fact': 'OLDRESTYLE',
            'decoration_style': 'WUSHE_BREEZE',
            'house_orientation': 'SOURTH',
            'remould_rooms': 3,
            'remould_livings': '1',
            'remould_kitchens': '1',
            'remould_bathrooms': '2',
            'remould_balconys': '2',
            'info_id': projectInfo[0],
            'module_type': 'projectOrder',
            'handle_type': 'updateApartment',
            "layout_attachs": {
                "attach_type": "LAYOUT",
                "imgs": [{
                    "url": img.url,
                    "img_id": img.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            },
            'zoneList': [
                {
                    "zone_type": "PUBLIC_TOILET",
                    "zone_type_name": "公共卫生间",
                    "room_no": "PUBLIC_TOILET_1",
                    "room_no_name": "公共卫生间1",
                    "zone_orientation": "NORTH",
                    "zone_orientation_name": "北",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "4",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "KITCHEN",
                    "zone_type_name": "厨房",
                    "room_no": "KITCHEN_1",
                    "room_no_name": "厨房",
                    "zone_orientation": "EAST",
                    "zone_orientation_name": "东",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "8",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "PARLOUR",
                    "zone_type_name": "客厅",
                    "room_no": "PARLOUR_1",
                    "room_no_name": "客厅1",
                    "zone_orientation": "EAST",
                    "zone_orientation_name": "东",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "16",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "ROOM",
                    "zone_type_name": "房间",
                    "room_no": "METH",
                    "room_no_name": "甲",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "HAVE",
                    "have_toilet_name": "有(4平米)",
                    "toilet_area": "4",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "11",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "ROOM",
                    "zone_type_name": "房间",
                    "room_no": "ETH",
                    "room_no_name": "乙",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "12",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "ROOM",
                    "zone_type_name": "房间",
                    "room_no": "PROP",
                    "room_no_name": "丙",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "13",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "BALCONY",
                    "zone_type_name": "阳台",
                    "room_no": "BALCONY_1",
                    "room_no_name": "阳台1",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(0平米)",
                    "window_area": "0",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "2",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                },
                {
                    "zone_type": "BALCONY",
                    "zone_type_name": "阳台",
                    "room_no": "BALCONY_2",
                    "room_no_name": "阳台2",
                    "zone_orientation": "SOURTH",
                    "zone_orientation_name": "南",
                    "have_toilet": "WITHOUT",
                    "have_toilet_name": "-",
                    "toilet_area": "0",
                    "have_balcony": "WITHOUT",
                    "have_balcony_name": "-",
                    "balcony_area": "0",
                    "have_window_name": "有(1平米)",
                    "window_area": "1",
                    "zone_status_name": "已创建",
                    "zone_status": "FOUND",
                    "usearea": "3",
                    "window_type": "ORDINARYWINDOW",
                    "zone_id": "",
                    "is_fictitious_room": "N"
                }
            ],
            'project_id': self.project_id,
            'project_no': projectInfo[1],
            'entrust_type': projectInfo[2]
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'项目方案制定完成')
            return

    # 物品清单
    def configList(self):

        # 制定物品清单
        def designConfigList():

            def getZoneId():
                url = 'http://decorate.ishangzu.com/isz_decoration/NewConfigurationController/queryZone/%s' % self.project_id
                result = myRequest(url, method='get')
                if result:
                    zoneInfo = result['obj']
                    for i in zoneInfo:
                        if i['function_zone'] == u'甲':
                            zoneId = i['zone_id']
                            return zoneId

            def confirm():
                zoneId = getZoneId()
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/confirm'
                data = [
                    {
                        "acceptance_num": None,
                        "acceptance_num_this": None,
                        "brand_id": None,
                        "brand_name": "爱上租定制",
                        "category_flag": None,
                        "category_one_id": None,
                        "category_one_len": None,
                        "category_one_nm": "家具",
                        "category_two_id": None,
                        "category_two_nm": "书桌",
                        "config_list_id": None,
                        "config_list_status": None,
                        "config_list_status_name": None,
                        "create_name": None,
                        "create_time": None,
                        "create_uid": None,
                        "deleted": None,
                        "flag": None,
                        "function_zone": "甲",
                        "function_zone_len": None,
                        "new_replenish_id": None,
                        "order_type": None,
                        "predict_delivery_date": None,
                        "project_id": self.project_id,
                        "purchase_num": "10",
                        "purchase_order_no": None,
                        "real_delivery_time": None,
                        "remark": None,
                        "remark_accept": None,
                        "remark_return": None,
                        "replacement_order": None,
                        "return_num": None,
                        "return_num_this": None,
                        "standard_id": None,
                        "standard_name": "0.86M（3.0）",
                        "submit_time": None,
                        "supplier_id": "8A2152435CF3FFF3015D0C64330F0011",
                        "supplier_name": "浙江品至家具有限公司",
                        "total_account": None,
                        "total_paid": 3100,
                        "unit_id": None,
                        "unit_name": "张",
                        "unit_price": 310,
                        "update_time": None,
                        "update_uid": None,
                        "zone_id": zoneId,
                        "index": 0,
                        "disabled": "true"
                    }
                ]
                result = myRequest(url, data)
                if result:
                    consoleLog(u'物品添加完成，准备下单')
                    return

            def submitOrder():
                confirm()
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/submitOrder'
                data = [{
                    "predict_delivery_date": '%s 00:00:00' % addDays(2),
                    "project_id": self.project_id,
                    "supplier_id": "8A2152435CF3FFF3015D0C64330F0011",
                    "supplier_name": "家具供应商:浙江品至家具有限公司"
                }]
                result = myRequest(url, data)
                if result:
                    consoleLog(u'物品清单下单完成')
                    return

            submitOrder()

        # 物品清单验收
        def acceptanceConfigList():

            #  获取物品清单信息
            def getsupplierOrderDetail():
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/supplierOrdersDetail'
                # supplierId = sqlbase.serach(
                supplierId = Mysql().getOne(
                    "select supplier_id from %s.new_config_list where project_id='%s' and deleted=0  and config_list_status<>'CHECKED'" % (
                        get_conf('db', 'decoration_db'), self.project_id))[0]
                data = {"project_id": self.project_id, "supplier_id": supplierId}
                result = myRequest(url, data)
                if result:
                    return result['obj']

            # 验收确认
            def acceptanceConfirm():
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/acceptance/confirm'
                data = getsupplierOrderDetail()
                for i in data:
                    i['real_delivery_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                result = myRequest(url, data)
                if result:
                    consoleLog(u'物品清单验收完成!')
                    return

            acceptanceConfirm()

        designConfigList()
        acceptanceConfigList()

    # 装修清单
    def stuffList(self):

        # commonData = [
        #     {
        #     "acceptance_num": None,
        #     "acceptance_num_this": 0,
        #     "acceptance_time": None,
        #     "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "create_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "data_type": "综合服务",
        #     "data_type_len": 3,
        #     "decoration_detial": "综合服务明细一",
        #     "deleted": 0,
        #     "function_zone": "客厅1",
        #     "function_zone_len": 7,
        #     "order_type": None,
        #     "predict_delivery_date": None,
        #     "project_id": self.project_id,
        #     "purchase_num": 10,
        #     "purchase_order_no": None,
        #     "remark": None,
        #     "remark_accept": None,
        #     "remark_detail": "",
        #     "remark_return": None,
        #     "replacement_order": None,
        #     "return_name": None,
        #     "return_num": None,
        #     "return_num_this": 0,
        #     "stuff_list_id": None,
        #     "stuff_list_status": "DRAFT",
        #     "submit_time": None,
        #     "supplier_id": '8A2152435FBAEFC3015FBAEFC3000000',
        #     "supplier_name": None,
        #     "total_account": None,
        #     "total_paid": 160,
        #     "unit_id": None,
        #     "unit_name": "测试单位",
        #     "unit_price": 16,
        #     "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "update_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "zone_type": None,
        #     "type_index": 0,
        #     "fun_index": 0
        # }, {
        #     "acceptance_num": None,
        #     "acceptance_num_this": 0,
        #     "acceptance_time": None,
        #     "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "create_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "data_type": "综合服务",
        #     "data_type_len": 3,
        #     "decoration_detial": "综合服务明细二",
        #     "deleted": 0,
        #     "function_zone": "客厅1",
        #     "function_zone_len": 7,
        #     "order_type": None,
        #     "predict_delivery_date": None,
        #     "project_id": self.project_id,
        #     "purchase_num": 10,
        #     "purchase_order_no": None,
        #     "remark": None,
        #     "remark_accept": None,
        #     "remark_detail": "",
        #     "remark_return": None,
        #     "replacement_order": None,
        #     "return_name": None,
        #     "return_num": None,
        #     "return_num_this": 0,
        #     "stuff_list_id": None,
        #     "stuff_list_status": "DRAFT",
        #     "submit_time": None,
        #     "supplier_id": None,
        #     "supplier_name": None,
        #     "total_account": None,
        #     "total_paid": 170,
        #     "unit_id": None,
        #     "unit_name": "测试单位",
        #     "unit_price": 17,
        #     "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "update_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "zone_type": None,
        #     "fun_index": 1,
        #     "type_index": 1
        # }, {
        #     "acceptance_num": None,
        #     "acceptance_num_this": 0,
        #     "acceptance_time": None,
        #     "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "create_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "data_type": "综合服务",
        #     "data_type_len": 3,
        #     "decoration_detial": "综合服务明细三",
        #     "deleted": 0,
        #     "function_zone": "客厅1",
        #     "function_zone_len": 7,
        #     "order_type": None,
        #     "predict_delivery_date": None,
        #     "project_id": self.project_id,
        #     "purchase_num": 10,
        #     "purchase_order_no": None,
        #     "remark": None,
        #     "remark_accept": None,
        #     "remark_detail": "",
        #     "remark_return": None,
        #     "replacement_order": None,
        #     "return_name": None,
        #     "return_num": None,
        #     "return_num_this": 0,
        #     "stuff_list_id": None,
        #     "stuff_list_status": "DRAFT",
        #     "submit_time": None,
        #     "supplier_id": None,
        #     "supplier_name": None,
        #     "total_account": None,
        #     "total_paid": 180,
        #     "unit_id": None,
        #     "unit_name": "测试单位",
        #     "unit_price": 18,
        #     "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "update_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "zone_type": None,
        #     "fun_index": 1,
        #     "type_index": 1
        # }, {
        #     "acceptance_num": None,
        #     "acceptance_num_this": 0,
        #     "acceptance_time": None,
        #     "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "create_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "data_type": "拆除",
        #     "data_type_len": 4,
        #     "decoration_detial": "拆除明细一",
        #     "deleted": 0,
        #     "function_zone": "客厅1",
        #     "function_zone_len": 7,
        #     "order_type": None,
        #     "predict_delivery_date": None,
        #     "project_id": self.project_id,
        #     "purchase_num": 10,
        #     "purchase_order_no": None,
        #     "remark": None,
        #     "remark_accept": None,
        #     "remark_detail": "",
        #     "remark_return": None,
        #     "replacement_order": None,
        #     "return_name": None,
        #     "return_num": None,
        #     "return_num_this": 0,
        #     "stuff_list_id": None,
        #     "stuff_list_status": "DRAFT",
        #     "submit_time": None,
        #     "supplier_id": None,
        #     "supplier_name": None,
        #     "total_account": None,
        #     "total_paid": 230,
        #     "unit_id": None,
        #     "unit_name": "测试单位",
        #     "unit_price": 23,
        #     "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "update_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "zone_type": None,
        #     "fun_index": 1,
        #     "type_index": 0
        # }, {
        #     "acceptance_num": None,
        #     "acceptance_num_this": 0,
        #     "acceptance_time": None,
        #     "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "create_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "data_type": "拆除",
        #     "data_type_len": 4,
        #     "decoration_detial": "拆除明细二",
        #     "deleted": 0,
        #     "function_zone": "客厅1",
        #     "function_zone_len": 7,
        #     "order_type": None,
        #     "predict_delivery_date": None,
        #     "project_id": self.project_id,
        #     "purchase_num": 10,
        #     "purchase_order_no": None,
        #     "remark": None,
        #     "remark_accept": None,
        #     "remark_detail": "",
        #     "remark_return": None,
        #     "replacement_order": None,
        #     "return_name": None,
        #     "return_num": None,
        #     "return_num_this": 0,
        #     "stuff_list_id": None,
        #     "stuff_list_status": "DRAFT",
        #     "submit_time": None,
        #     "supplier_id": None,
        #     "supplier_name": None,
        #     "total_account": None,
        #     "total_paid": 240,
        #     "unit_id": None,
        #     "unit_name": "测试单位",
        #     "unit_price": 24,
        #     "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "update_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "zone_type": None,
        #     "fun_index": 1,
        #     "type_index": 1
        # }, {
        #     "acceptance_num": None,
        #     "acceptance_num_this": 0,
        #     "acceptance_time": None,
        #     "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "create_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "data_type": "拆除",
        #     "data_type_len": 4,
        #     "decoration_detial": "拆除明细三",
        #     "deleted": 0,
        #     "function_zone": "客厅1",
        #     "function_zone_len": 7,
        #     "order_type": None,
        #     "predict_delivery_date": None,
        #     "project_id": self.project_id,
        #     "purchase_num": 10,
        #     "purchase_order_no": None,
        #     "remark": None,
        #     "remark_accept": None,
        #     "remark_detail": "",
        #     "remark_return": None,
        #     "replacement_order": None,
        #     "return_name": None,
        #     "return_num": None,
        #     "return_num_this": 0,
        #     "stuff_list_id": None,
        #     "stuff_list_status": "DRAFT",
        #     "submit_time": None,
        #     "supplier_id": None,
        #     "supplier_name": None,
        #     "total_account": None,
        #     "total_paid": 250,
        #     "unit_id": None,
        #     "unit_name": "测试单位",
        #     "unit_price": 25,
        #     "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        #     "update_uid": "8A2152435DC1AEAA015DDE96F9276279",
        #     "zone_type": None,
        #     "fun_index": 1,
        #     "type_index": 1
        # }]
        commonData = [
            {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "create_uid": User.UID,
                "data_type": "成品安装",
                "data_type_len": 26,
                "decoration_detial": "家具安装",
                "deleted": 0,
                "function_zone": "甲",
                "function_zone_len": 100,
                "hard_deliver_audit_status": None,
                "order_type": None,
                "predict_delivery_date": None,
                "project_id": self.project_id,
                "purchase_num": "10",
                "purchase_order_no": None,
                "remark": None,
                "remark_accept": None,
                "remark_detail": "",
                "remark_return": None,
                "replacement_order": None,
                "return_name": None,
                "return_num": None,
                "return_num_this": 0,
                "stuff_fees_change_reason": None,
                "stuff_list_id": None,
                "stuff_list_status": "DRAFT",
                "submit_time": None,
                "supplier_id": None,
                "supplier_name": None,
                "total_account": None,
                "total_paid": "100.00",
                "unit_id": None,
                "unit_name": "件",
                "unit_price": 10,
                "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "update_uid": User.UID,
                "zone_type": None,
                "type_index": 0,
                "fun_index": 0
            }, {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "create_uid": User.UID,
                "data_type": "成品安装",
                "data_type_len": 26,
                "decoration_detial": "嵌入式天花灯-改造",
                "deleted": 0,
                "function_zone": "甲",
                "function_zone_len": 100,
                "hard_deliver_audit_status": None,
                "order_type": None,
                "predict_delivery_date": None,
                "project_id": self.project_id,
                "purchase_num": "11",
                "purchase_order_no": None,
                "remark": None,
                "remark_accept": None,
                "remark_detail": "",
                "remark_return": None,
                "replacement_order": None,
                "return_name": None,
                "return_num": None,
                "return_num_this": 0,
                "stuff_fees_change_reason": None,
                "stuff_list_id": None,
                "stuff_list_status": "DRAFT",
                "submit_time": None,
                "supplier_id": None,
                "supplier_name": None,
                "total_account": None,
                "total_paid": "264.00",
                "unit_id": None,
                "unit_name": "个",
                "unit_price": 24,
                "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "update_uid": User.UID,
                "zone_type": None,
                "fun_index": 1,
                "type_index": 1
            }, {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "create_uid": User.UID,
                "data_type": "成品安装",
                "data_type_len": 26,
                "decoration_detial": "明装筒灯-改造",
                "deleted": 0,
                "function_zone": "甲",
                "function_zone_len": 100,
                "hard_deliver_audit_status": None,
                "order_type": None,
                "predict_delivery_date": None,
                "project_id": self.project_id,
                "purchase_num": "12",
                "purchase_order_no": None,
                "remark": None,
                "remark_accept": None,
                "remark_detail": "",
                "remark_return": None,
                "replacement_order": None,
                "return_name": None,
                "return_num": None,
                "return_num_this": 0,
                "stuff_fees_change_reason": None,
                "stuff_list_id": None,
                "stuff_list_status": "DRAFT",
                "submit_time": None,
                "supplier_id": None,
                "supplier_name": None,
                "total_account": None,
                "total_paid": "403.20",
                "unit_id": None,
                "unit_name": "个",
                "unit_price": 33.6,
                "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "update_uid": User.UID,
                "zone_type": None,
                "fun_index": 1,
                "type_index": 1
            }
        ]

        # 制定装修清单
        def designStuffList():

            def preview():
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/preview'
                data = commonData
                result = myRequest(url, data)
                if result:
                    return

            def saveStuffLists():
                preview()
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/saveStuffLists'
                # projectInfo = sqlbase.serach(
                projectInfo = Mysql().getOne(
                    "select b.address,a.config_order_no,b.contract_id,b.contract_num,b.create_time,b.entrust_end_date,b.entrust_start_date,b.house_code,b.housekeep_mange_uid,b.info_id,"
                    "a.project_no,b.sign_date,b.city_code,b.city_name from %s.decoration_house_info b inner join  %s.new_decoration_project a on a.info_id=b.info_id and a.project_id='%s'" % (
                        get_conf('db', 'decoration_db'), get_conf('db', 'decoration_db'), self.project_id))
                data = {
                    "newStuffList": commonData,
                    "project": {
                        "address": projectInfo[0],
                        "build_area": "120.00",
                        "cable_laying_type": "INNERPIPEINNERLINE",
                        "cable_laying_type_name": None,
                        "city_code": "330100",
                        "city_name": "杭州市",
                        "closed_water_test_result": "Y",
                        "complete_two_nodes": "[\"VOLUME_SCORE\",\"SURVEY_PROPERTY_DELIVERY\",\"WATER_CLOSED_TEST\",\"PROJECT_PLAN\",\"GOODS_CONFIG_LIST\"]",
                        "complete_two_nodes_list": ["VOLUME_SCORE", "SURVEY_PROPERTY_DELIVERY", "WATER_CLOSED_TEST",
                                                    "PROJECT_PLAN", "GOODS_CONFIG_LIST"],
                        "config_list_status": "CHECKED",
                        "config_list_status_name": "已验收",
                        "config_order_no": projectInfo[1],
                        "config_progress": "WAIT_DESIGN",
                        "config_progress_name": "待设计",
                        "config_submit_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "config_submit_uid": User.UID,
                        "config_submit_uname": User.NAME,
                        "construct_uid": "1610",
                        "construct_uname": "徐经纬",
                        "construct_uname_phone": "徐经纬/13105715060",
                        "contract_id": projectInfo[2],
                        "contract_num": projectInfo[3],
                        "contract_type": "NEWSIGN",
                        "contract_type_name": "新签",
                        "create_time": projectInfo[4],
                        "create_uid": "8AEF8688600F30F30160257579287F96",
                        "current_one_node": "PROJECT_PLAN",
                        "decoration_style": "WUSHE_BREEZE",
                        "decoration_style_name": "随寓和风",
                        "deleted": 0,
                        "deliver_room_date": "1970-01-02 00:00:00.0",
                        "dispach_remark": "测试",
                        "entrust_end_date": projectInfo[5],
                        "entrust_start_date": projectInfo[6],
                        "entrust_type_fact": "SHARE",
                        "entrust_type_fact_name": "合租",
                        "grade": 20,
                        "hidden_check_date": "1970-01-02 00:00:00.0",
                        "house_code": projectInfo[7],
                        "housekeep_mange_name": None,
                        "housekeep_mange_uid": projectInfo[8],
                        "info_id": projectInfo[9],
                        "is_active": "Y",
                        "is_active_name": "是",
                        "one_level_nodes": "[\"PLACE_ORDER\",\"DISPATCH_ORDER\",\"SURVEY\",\"PROJECT_PLAN\",\"CONSTRUCTING\",\"PROJECT_CHECK\",\"PROJECT_COMPLETION\"]",
                        "order_status_name": "进程中",
                        "order_type_name": "新收配置订单",
                        "overall_check_date": "1970-01-02 00:00:00.0",
                        "phone": "18815286582",
                        "place_order_date": "2018-03-20 20:47:38",
                        "place_order_dep": "",
                        "place_order_dep_name": None,
                        "place_order_reason": "测试",
                        "place_order_uid": User.UID,
                        "place_order_uname": User.NAME,
                        "plumbing_type": "INNERPIPE",
                        "plumbing_type_name": None,
                        "predict_complete_date": "",
                        "predict_days": 0,
                        "predict_hidden_check_date": '%s 00:00:00' % addDays(2),
                        "predict_overall_check_date": '%s 00:00:00' % addDays(2),
                        "predict_stuff_check_date": '%s 00:00:00' % addDays(2),
                        "predict_survey_date": '%s 09:00:00' % addDays(2),
                        "project_id": self.project_id,
                        "project_no": projectInfo[10],
                        "project_order_status": "INPROCESS",
                        "project_order_type": "NEW_COLLECT_ORDER",
                        "reform_way": "OLDRESTYLE",
                        "reform_way_fact": "OLDRESTYLE",
                        "reform_way_fact_name": "老房全装",
                        "reform_way_name": "老房全装",
                        "remark": "",
                        "room_toilet": "3/2",
                        "sign_date": projectInfo[11],
                        "sign_name": None,
                        "sign_uid": "8A2152435DC1AEAA015DDE96F9276279",
                        "sign_user_phone": None,
                        "start_time": '%s 00:00:00' % addDays(2),
                        "stuff_check_date": "1970-01-02 00:00:00.0",
                        "stuff_list_status": "DRAFT",
                        "stuff_list_status_name": "待下单",
                        "stuff_order_no": "",
                        "stuff_submit_time": "1970-01-02 00:00:00.0",
                        "stuff_submit_uid": "",
                        "stuff_submit_uname": "",
                        "supplier_id": "8A2152435FBAEFC3015FBAEFC3000000",
                        "supplier_name": "测试专用硬装供应商",
                        "supplier_uid": "8AB398CA5FBAF072015FBB26338A0002",
                        "supplier_uname": "测试专用硬装员工",
                        "supplier_uname_phone": "测试专用硬装员工/18815286582",
                        "timeMap": None,
                        "total_paid": 0,
                        "two_level_nodes": "[\"VOLUME_SCORE\",\"SURVEY_PROPERTY_DELIVERY\",\"WATER_CLOSED_TEST\",\"DECORATION_CONFIG_LIST\",\"GOODS_CONFIG_LIST\",\"PROJECT_PLAN\",\"CONCEALMENT_ACCEPTANCE\",\"HARD_ACCEPTANCE\",\"ACCEPTANCE_PROPERTY_DELIVERY\",\"COST_SETTLEMENT\",\"OVERALL_ACCEPTANCE\",\"HOUSE_DELIVERY\",\"INDOOR_PICTURE\"]",
                        "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "update_uid": "8AEF8688600F30F30160257579287F96",
                        "wall_condition": "OLDHOUSE",
                        "wall_condition_name": None
                    }
                }
                result = myRequest(url, data)
                if result:
                    consoleLog(u'装修清单制定完成')
                    return

            saveStuffLists()

        # 装修清单验收
        def acceptanceStuffList():
            geturl = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/getSuffList/%s' % self.project_id
            result = myRequest(geturl, method='get')
            if result:
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/acceptanceAll'
                acceptance_time = time.strftime('%Y-%m-%d %H:%M:%S')
                data = result['obj']['newStuffList']
                for stufflist in data:
                    stufflist['acceptance_time'] = acceptance_time
                    stufflist['acceptance_num_this'] = stufflist['purchase_num']
                result = myRequest(url, data)
                if result:
                    consoleLog(u'装修清单验收完成')
                    return

        designStuffList()
        acceptanceStuffList()

    # 施工中
    def hideAndStufCheck(self):

        def hideCheck():
            """隐蔽验收"""
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/constructing/hideCheck'
            data = {
                "air_switch": None,
                "attachments": [{
                    "attach_type": "TOILET",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 0,
                        "type": "TOILET"
                    }]
                }, {
                    "attach_type": "KITCHEN",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 1,
                        "type": "KITCHEN"
                    }]
                }, {
                    "attach_type": "LIVING_ROOM",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 2,
                        "type": "LIVING_ROOM"
                    }]
                }, {
                    "attach_type": "BALCONY",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 3,
                        "type": "BALCONY"
                    }]
                }, {
                    "attach_type": "OTHER",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 4,
                        "type": "OTHER"
                    }]
                }],
                "check_remark": "",
                "closed_water_test_result": None,
                "curOneLevelNode": None,
                "curTwoLevelNode": None,
                "door_card": None,
                "door_key": None,
                "electricity_card": None,
                "electricity_meter_num": None,
                "electricity_meter_remain": None,
                "gas_card": None,
                "gas_meter_num": None,
                "gas_meter_remain": None,
                "grade": None,
                "hidden_check_date": '%s 09:00:00' % addDays(1),
                "landlordGoods": None,
                "project_id": self.project_id,
                "reform_way_fact": None,
                "reform_way_fact_name": "",
                "remark": None,
                "score_remark": None,
                "water_card": None,
                "water_card_remain": None,
                "water_meter_num": None
            }
            for attachment in data['attachments']:
                IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % attachment['attach_type'],
                                  filepath=r"C:\Users\user\Desktop\Image\\")
                attachment['imgs'][0]['url'] = IMG.url
                attachment['imgs'][0]['img_id'] = IMG.id
            result = myRequest(url, data)
            if result:
                consoleLog(u'隐蔽验收完成')
                return

        # 硬装验收
        def stufCheck():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/constructing/stufCheck'
            data = {
                "air_switch": None,
                "attachments": [{
                    "attach_type": "TOILET",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 0,
                        "type": "TOILET"
                    }]
                }, {
                    "attach_type": "KITCHEN",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 1,
                        "type": "KITCHEN"
                    }]
                }, {
                    "attach_type": "LIVING_ROOM",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 2,
                        "type": "LIVING_ROOM"
                    }]
                }, {
                    "attach_type": "ROOM",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 3,
                        "type": "ROOM"
                    }]
                }, {
                    "attach_type": "OTHER",
                    "imgs": [{
                        "url": get_conf('img', 'url'),
                        "img_id": get_conf('img', 'img_id'),
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 4,
                        "type": "OTHER"
                    }]
                }],
                "check_remark": "",
                "closed_water_test_result": None,
                "curOneLevelNode": None,
                "curTwoLevelNode": None,
                "door_card": None,
                "door_key": None,
                "electricity_card": None,
                "electricity_meter_num": None,
                "electricity_meter_remain": None,
                "gas_card": None,
                "gas_meter_num": None,
                "gas_meter_remain": None,
                "grade": None,
                "hidden_check_date": None,
                "stuff_check_date": '%s 09:00:00' % addDays(1),
                "landlordGoods": None,
                "project_id": self.project_id,
                "reform_way_fact": None,
                "reform_way_fact_name": "",
                "remark": None,
                "score_remark": None,
                "water_card": None,
                "water_card_remain": None,
                "water_meter_num": None
            }
            for attachment in data['attachments']:
                IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % attachment['attach_type'],
                                  filepath=r"C:\Users\user\Desktop\Image\\")
                attachment['imgs'][0]['url'] = IMG.url
                attachment['imgs'][0]['img_id'] = IMG.id
            result = myRequest(url, data)
            if result:
                consoleLog(u'硬装验收完成')
                return

        hideCheck()
        stufCheck()

    # 项目验收
    def projectCheck(self):
        # 整体验收
        def wholeCheck():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/wholeCheck'
            IMG_CARDS = upLoadPhoto(url=self.uploadPhotoURL, filename='CARDS.png',
                                    filepath=r"C:\Users\user\Desktop\Image\\")
            IMG_THREE = upLoadPhoto(url=self.uploadPhotoURL, filename='THREE.png',
                                    filepath=r"C:\Users\user\Desktop\Image\\")
            data = {
                "air_switch": None,
                "attachments": None,
                "card_attachs": [{
                    "attach_type": "CARDS",
                    "imgs": [{
                        "url": IMG_CARDS.url,
                        "img_id": IMG_CARDS.id,
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 0,
                        "type": ""
                    }]
                }],
                "closed_water_test_result": None,
                "curOneLevelNode": None,
                "curTwoLevelNode": None,
                "door_card": None,
                "door_key": None,
                "electricity_card": None,
                "electricity_meter_num": None,
                "electricity_meter_remain": None,
                "gas_card": None,
                "gas_meter_num": None,
                "gas_meter_remain": None,
                "grade": None,
                "landlordGoods": None,
                "newStuffList": None,
                "overall_check_date": '%s 10:00:00' % addDays(1),
                "project_id": self.project_id,
                "remark": "",
                "score_remark": None,
                "three_attachs": [{
                    "attach_type": "THREE",
                    "imgs": [{
                        "url": IMG_THREE.url,
                        "img_id": IMG_THREE.id,
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 0,
                        "type": ""
                    }]
                }],
                "water_card": None,
                "water_card_remain": None,
                "water_meter_num": None
            }
            result = myRequest(url, data)
            if result:
                # consoleLog(u'整体验收完成')
                return

        # 物业交割验收
        def profee():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/profee'
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='PROPERTY_DELIVERY_ORDER.png',
                              filepath=r"C:\Users\user\Desktop\Image\\")
            data = {
                "air_switch": "",
                "door_card": "",
                "door_key": "",
                "electricity_card": "",
                "electricity_meter_num": "",
                "electricity_meter_remain": "",
                "gas_card": "",
                "gas_meter_num": "",
                "gas_meter_remain": "",
                "project_id": self.project_id,
                "water_card": "",
                "water_card_remain": "",
                "water_meter_num": "",
                "attachments": [{
                    "attach_type": "PROPERTY_DELIVERY_ORDER",
                    "imgs": [{
                        "url": IMG.url,
                        "img_id": IMG.id,
                        "create_name": "",
                        "create_dept": "",
                        "create_time": "",
                        "sort": 0,
                        "type": ""
                    }]
                }],
                "resource": "PROJECT_CHECK"
            }
            result = myRequest(url, data)
            if result:
                # consoleLog(u'物业交割完成')
                return

        # 费用结算
        def costSettle():
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/costsettle'
            data = {
                "project_id": self.project_id,
                "remark": ""
            }
            result = myRequest(url, data)
            if result:
                # consoleLog(u'费用结算完成')
                return

        wholeCheck()
        profee()
        costSettle()

    # 室内图
    def indoorImg(self):
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/indoor'
        # IMG_PUBLIC_TOILET_1 = upLoadPhoto(url=self.uploadPhotoURL, filename='PUBLIC_TOILET_1.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_KITCHEN_1 = upLoadPhoto(url=self.uploadPhotoURL, filename='KITCHEN_1.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_PARLOUR_1 = upLoadPhoto(url=self.uploadPhotoURL, filename='PARLOUR_1.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_METH = upLoadPhoto(url=self.uploadPhotoURL, filename='METH.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_ETH = upLoadPhoto(url=self.uploadPhotoURL, filename='ETH.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_PROP = upLoadPhoto(url=self.uploadPhotoURL, filename='PROP.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_BALCONY_1 = upLoadPhoto(url=self.uploadPhotoURL, filename='BALCONY_1.png', filepath=r"C:\Users\user\Desktop\Image\\")
        # IMG_BALCONY_2 = upLoadPhoto(url=self.uploadPhotoURL, filename='BALCONY_2.png', filepath=r"C:\Users\user\Desktop\Image\\")
        IMG_LAYOUT = upLoadPhoto(url=self.uploadPhotoURL, filename='LAYOUT.png',
                                 filepath=r"C:\Users\user\Desktop\Image\\")
        data = {
            "curOneLevelNode": None,
            "curTwoLevelNode": None,
            "deliver_room_date": None,
            "house_attachs": [{
                "attach_type": "PUBLIC_TOILET_1",
                "imgs": [{
                    "url": None,  # IMG_PUBLIC_TOILET_1.url,
                    "img_id": None,  # IMG_PUBLIC_TOILET_1.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": "PUBLIC_TOILET_1"
                }]
            }, {
                "attach_type": "KITCHEN_1",
                "imgs": [{
                    "url": None,  # IMG_KITCHEN_1.url,
                    "img_id": None,  # IMG_KITCHEN_1.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 1,
                    "type": "KITCHEN_1"
                }]
            }, {
                "attach_type": "PARLOUR_1",
                "imgs": [{
                    "url": None,  # IMG_PARLOUR_1.url,
                    "img_id": None,  # IMG_PARLOUR_1.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 2,
                    "type": "PARLOUR_1"
                }]
            }, {
                "attach_type": "METH",
                "imgs": [{
                    "url": None,  # IMG_METH.url,
                    "img_id": None,  # IMG_METH.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 3,
                    "type": "METH"
                }]
            }, {
                "attach_type": "ETH",
                "imgs": [{
                    "url": None,  # IMG_ETH.url,
                    "img_id": None,  # IMG_ETH.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 4,
                    "type": "ETH"
                }]
            }, {
                "attach_type": "PROP",
                "imgs": [{
                    "url": None,  # IMG_PROP.url,
                    "img_id": None,  # IMG_PROP.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 5,
                    "type": "PROP"
                }]
            }, {
                "attach_type": "BALCONY_1",
                "imgs": [{
                    "url": None,  # IMG_BALCONY_1.url,
                    "img_id": None,  # IMG_BALCONY_1.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 6,
                    "type": "BALCONY_1"
                }]
            }, {
                "attach_type": "BALCONY_2",
                "imgs": [{
                    "url": None,  # IMG_BALCONY_2.url,
                    "img_id": None,  # IMG_BALCONY_2.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 7,
                    "type": "BALCONY_2"
                }]
            }],
            "layout_attachs": [{
                "attach_type": "LAYOUT",
                "imgs": [{
                    "url": IMG_LAYOUT.url,
                    "img_id": IMG_LAYOUT.id,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": ""
                }]
            }],
            "project_id": self.project_id,
            "remark": None
        }
        for house_attach in data['house_attachs']:
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % house_attach['attach_type'],
                              filepath=r"C:\Users\user\Desktop\Image\\")
            house_attach['imgs'][0]['url'] = IMG.url
            house_attach['imgs'][0]['img_id'] = IMG.id
        result = myRequest(url, data)
        if result:
            # consoleLog(u'室内图添加完成')
            return

    # 竣工交付
    def delivery(self):
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/delivery'
        data = {
            "deliver_room_date": '%s 10:00:00' % addDays(1),
            "project_id": self.project_id,
            "remark": ""
        }
        result = myRequest(url, data)
        if result:
            consoleLog('————————竣工完成————————')
            return

    # 整个装修流程
    def fitment(self):
        self.newPlaceOrder()  # 下单
        self.newDispatchOrder()  # 派单
        self.newAcceptOrder()  # PC接单
        self.newSurvey()  # 量房
        # self.appAcceptOrder()  # 接单
        # self.placeOrder()  # 下单
        # self.dispatchOrder()  # 派单
        # self.acceptOrder()  # 接单
        # self.survey()  # 勘测
        # self.projectOrder()  # 项目计划
        # self.configList()  # 物品清单
        # self.stuffList()  # 装修清单
        # self.hideAndStufCheck()  # 施工中
        # self.projectCheck()  # 项目验收
        # self.indoorImg()  # 室内图
        # self.delivery()  # 竣工

    @staticmethod
    # def decorationAppLogin(user=get_conf('sysUser', 'userPhone'), password=get_conf('sysUser', 'pwd')):
    def decorationAppLogin(user_type='employee', user=get_conf('sysUser', 'userPhone'),
                           password=get_conf('sysUser', 'pwd')):
        data = {}
        if user_type == 'employee':  # 专员登录
            user_type = 'employee/EmployeeLoginController'
            # data = {"user_phone": "15168368432", "user_pwd": password}
            data = {"user_phone": "13600000003", "user_pwd": password}
            # data = {"user_phone": "15606513905", "user_pwd": 'isz123456'}
        elif user_type == 'supplier':  # 供应商登录
            user_type = 'supplier/LoginController'
            data = {"phone": "18815286582", "password": '123456'}
        url = 'http://decorationapp.ishangzu.com/isz_decorationapp/%s/login' % user_type
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        result = json.loads(response.text)
        if result['msg'] == u'ok':
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            decorationapp_cookies = {
                "SESSION_KEY_DECORATIONAPP_EMPLOYEE": cookies.get('SESSION_KEY_DECORATIONAPP_EMPLOYEE'),
                "SESSION_KEY_DECORATIONAPP": cookies.get('SESSION_KEY_DECORATIONAPP')
            }
            set_conf('cookieInfo', decorationapp_cookies=decorationapp_cookies)
            consoleLog(u'工程移动端登录成功!')
        elif u'密码错误' in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            quit()

    def supplierAcceptOrder(self):
        url = "http://decorationapp.ishangzu.com/isz_decorationapp/supplier/SupplierWaitAcceptOrderController/supplierAcceptOrder"
        data = {"project_id": self.project_id, "taskId": self.taskId, "predict_survey_date": self.predict_survey_date}
        result = myRequest(url, data, method='put')
        if result:
            consoleLog("供应商接单成功")
        else:
            consoleLog("供应商接单失败", 'e')

    def constructAcceptOrder(self):
        url = "http://decorationapp.ishangzu.com/isz_decorationapp/employee/WaitAcceptOrderController/constructAcceptOrder"
        data = {"project_id": self.project_id, "predict_survey_date": '%s 09:00' % addDays(1)}
        result = myRequest(url, data, method='put')
        if result:
            consoleLog("专员接单成功")
        else:
            consoleLog("专员接单失败", 'e')

    def appAcceptOrder(self):
        self.decorationAppLogin('employee')
        self.constructAcceptOrder()
        self.decorationAppLogin('supplier')
        self.supplierAcceptOrder()

    def newSurvey(self):
        """量房"""
        upLoadPhotoURL = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/DecorationFileController/uploadPhoto'
        IMG = upLoadPhoto(url=upLoadPhotoURL, filename='PROPERTY_DELIVERY_ORDER.png', filepath=r"C:\Users\user\Desktop\Image\\")

        def saveSurveyStatus():
            """量房通过"""
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/decorationSurveyController/saveSurveyStatus'
            data = {
                "project_id": self.project_id,
                "survery_room_status": "118",
                "survery_room_status_description": ""
            }
            result = myRequest(url, data, returnValue=True)
            if result:
                consoleLog("量房通过")
            else:
                raise Exception("量房不通过")

        def searchSurveyBaseInfo():
            """获取房源基本信息"""
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/decorationSurveyController/searchSurveyBaseInfo'
            data = {"project_id": self.project_id}
            result = myRequest(url, data)
            if result:
                self.timestamp = result['obj']['update_timestamp']
                return result['obj']
            else:
                raise Exception("获取订单基础信息失败")

        def dividedHouse():
            """分割户型"""
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/decorationSurveyController/saveSurveyBaseInfo'
            data = searchSurveyBaseInfo()
            data['house_orientation'] = 'SOURTH'
            data['house_type'] = 'HOUSE'
            data['decoration_style'] = 'WITHOUT'
            data['is_need_waterproofing'] = 'Y'
            data['optimization_room'] = 'ZERO'
            data['original_wall'] = 'WHITE_WALL_WHITE_TOP'
            data['reform_way_fact'] = 'RESTYLED'
            data['remould_balconys'] = '0'
            data['remould_bathrooms'] = '0'
            data['remould_kitchens'] = '0'
            data['remould_livings'] = '1'
            data['remould_rooms'] = '1'
            result = myRequest(url, data)
            if result:
                pass
            else:
                raise Exception("户型分割失败！")

        def getStuffList(function_area, is_fictitious_room='N'):
            """获取装修项目"""
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/StuffListController/getStuffList'
            data = {"exist_ids": "", "function_area": function_area, "project_id": self.project_id,
                    "is_fictitious_room": is_fictitious_room}
            result = myRequest(url, data)
            if result:
                if len(result['obj']) > 0:
                    if len(result['obj'][0]) > 0:
                        if len(result['obj'][0]['product_detail']) > 0:
                            return result['obj'][0]['product_detail'][0]
                else:
                    consoleLog("未获取到装修项目")
                    return None
            else:
                raise Exception("获取装修项目失败！")

        def getProductList(is_fictitious_room='N'):
            """获取配置物品"""
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/ConfigListController/getProductList'
            data = {"exist_ids": "", "product_name": "", "project_id": self.project_id,
                    "is_fictitious_room": is_fictitious_room}
            result = myRequest(url, data)
            if result:
                if len(result['obj']['rows']) > 0:
                    if len(result['obj']['rows'][0]) > 0:
                        if len(result['obj']['rows'][0]['decorationProductPageVoList']) > 0:
                            return result['obj']['rows'][0]['decorationProductPageVoList'][0]
                else:
                    consoleLog("未获取到配置物品")
                    return None
            else:
                raise Exception("获取配置物品失败！")

        def updateFunctionZone(zone_id, zone_type, room_no):
            """更新区间信息"""
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/decorationFunctionZoneController/updateFunctionZone'
            data = {
                "have_balcony": "WITHOUT",
                "have_toilet": "WITHOUT",
                "info_id": self.info_id,
                "is_fictitious_room": "N",
                "is_suite": True,
                "room_no": room_no,
                "usearea": "12",
                "window_type": "WITHOUT",
                "window_area": "",
                "zone_id": zone_id,
                "zone_orientation": "SOURTH",
                "zone_type": zone_type
            }
            result = myRequest(url, data)
            if result:
                pass
            else:
                raise Exception("功能区间信息更新失败！")

        def addStuffAndProduct():
            """房屋添加硬装和配置"""
            houseInfo = searchSurveyBaseInfo()
            product = getProductList()
            zones = houseInfo['zoneVoList']
            for index, zoneInfo in enumerate(zones):
                stuff = getStuffList(zoneInfo.get('zone_type'))
                if not zoneInfo.get('zone_type') == 'SPORADIC':
                    updateFunctionZone(zoneInfo['zone_id'], zoneInfo['zone_type'], zoneInfo['room_no'])
                    zoneInfo['have_window_name'] = '无'
                    zoneInfo['usearea'] = '12'
                    zoneInfo['window_type'] = 'WITHOUT'
                    zoneInfo['zone_orientation'] = 'SOURTH'
                    zoneInfo['zone_orientation_name'] = '南'
                    if product:
                        product['purchase_num'] = 1
                        product['change_type'] = 'ADD'
                        product['zone_id'] = zoneInfo['zone_id']
                        product['function_zone'] = zoneInfo['room_no_name']
                        zoneInfo['products'] = [product]
                    if stuff:
                        stuff['change_type'] = 'ADD'
                        stuff['purchase_num'] = 10
                        stuff['function_zone'] = zoneInfo['room_no_name']
                        stuff['zone_id'] = zoneInfo['zone_id']
                        zoneInfo['stuffList'] = [stuff]
                zones[index] = zoneInfo
            houseInfo['zoneVoList'] = zones
            return houseInfo

        def save(data):
            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/MongoController/save'

            data['property_attachments'] = [{
                "img_url": IMG.url,
                "img_id": IMG.id
            }]
            data = {"key": "SaveAmountRooms_{}_{}".format(self.timestamp, self.project_id), "value": data}
            result = myRequest(url, data)
            if result:
                pass
            else:
                raise Exception("提交失败！")

        def saveSurveyStuffConfig():
            """提交量房"""

            url = 'http://decorationapp.ishangzu.com/isz_decorationapp/employee/decorationSurveyController/saveSurveyStuffConfig'
            zoneVoList = addStuffAndProduct()['zoneVoList']
            data = {
                "layout_attachments": {
                    "attach_type": "LAYOUT",
                    "imgs": []
                },
                "property_attachments": [{
                    "img_url": IMG.url,
                    "img_id": IMG.id
                }],
                "project_id": self.project_id,
                "start_date": today(),
                "taskId": self.task_Id,
                "zoneSCInfoDTOS": zoneVoList,
                "survery_room_result": "success",
                "check_data_type": "NORMAL"
            }
            result = myRequest(url, data)
            if result:
                pass
            else:
                raise Exception("提交失败！")

        saveSurveyStatus()
        dividedHouse()
        save(addStuffAndProduct())
        # saveSurveyStuffConfig()


if __name__ == '__main__':
    project = Decoration("WFL-2.0BS11271604-hI")
    Decoration.decorationAppLogin(user_type='employee')
    # project.appAcceptOrder()
    project.newSurvey()

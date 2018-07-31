# -*- coding:utf8 -*-

import time
from common import sqlbase
from common.base import consoleLog, get_conf
from common.datetimes import addDays
from common.interface_wfl import myRequest, upLoadPhoto
from common.dict import UserInfo, get_dict_value
from isz.infoClass import DecorationProjectInfo


class Decoration(DecorationProjectInfo):
    """装修工程"""
    uploadPhotoURL = 'http://decorate.ishangzu.com/isz_decoration/DecorationFileController/uploadPhoto'  # 装修工程上传图片地址
    user = UserInfo.getConfigUser()

    def placeOrder(self):
        """下单"""
        consoleLog(u'开始工程管理')
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/placeOrder'
        data = {
            'place_order_dep': self.user.dep_id,
            'place_order_reason': u'测试',
            'place_order_uid': self.user.user_id,
            'place_order_uname': self.user.user_name,
            'place_order_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'predict_survey_date': '%s 09:00' % addDays(1),
            'project_id': self.project_id
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'下单完成')
            return

    def dispatchOrder(self):
        """派单"""
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/dispatchOrder'
        data = {
            'construct_uid': '1610',
            'construct_uname': u'徐经纬',
            'dispach_remark': u'测试派单',
            'project_id': self.project_id,
            'supplier_id': '8A2152435FBAEFC3015FBAEFC3000000',
            'supplier_uid': '8AB398CA5FBAF072015FBB26338A0002',
            'predict_survey_date': '',
            'supplier_name': u'测试专用硬装供应商',
            'supplier_uname': u'测试专用硬装员工'
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'派单完成')
            return

    def acceptOrder(self):
        """接单"""
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/changeProgress/acceptOrder'
        data = {
            'project_id': self.project_id,
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'接单完成')
            return

    def survey(self, is_need_waterproofing='Y'):
        """量房"""

        def score():
            """测量"""
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/score'
            data = {
                'grade': '20',
                'project_id': self.project_id,
                'reform_way_fact': 'REFORM',
                'score_remark': '',
                'attachments': [{
                    'attach_type': 'TOILET',
                    'imgs': [{
                        "url": None,
                        "img_id": None,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 0,
                        'type': 'TOILET'
                    }]
                }, {
                    'attach_type': 'KITCHEN',
                    'imgs': [{
                        "url": None,
                        "img_id": None,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 1,
                        'type': 'KITCHEN'
                    }]
                }, {
                    'attach_type': 'LIVING_ROOM',
                    'imgs': [{
                        'url': None,
                        'img_id': None,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 2,
                        'type': 'LIVING_ROOM'
                    }]
                }, {
                    'attach_type': 'ROOM',
                    'imgs': [{
                        "url": None,
                        "img_id": None,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 3,
                        'type': 'ROOM'
                    }]
                }, {
                    'attach_type': 'OTHER',
                    'imgs': [{
                        "url": None,
                        "img_id": None,
                        'create_name': '',
                        'create_dept': '',
                        'create_time': '',
                        'sort': 4,
                        'type': 'OTHER'
                    }]
                }]
            }
            for attachment in data['attachments']:
                IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % attachment['attach_type'])
                attachment['imgs'][0]['url'] = IMG.url
                attachment['imgs'][0]['img_id'] = IMG.id
            result = myRequest(url, data)
            if result:
                # consoleLog(u'测量完成')
                return

        def profee():
            """物业交割"""
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/survey/profee'
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='PROPERTY_DELIVERY_ORDER.png')
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

        def closed():
            """闭水"""
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

    def projectOrder(self, rooms=3, livings=1, kitchens=1, bathrooms=2, balconys=2):
        """项目计划"""
        url = 'http://decorate.ishangzu.com/isz_decoration/decoHouseInfoController/saveOrUpdateApartment/saveApartment/projectOrder'
        img = upLoadPhoto(url=self.uploadPhotoURL, filename='LAYOUT.png')  # 户型图上传
        data = {
            'build_area': self.build_area,
            'reform_way_fact': 'OLDRESTYLE',
            'decoration_style': 'WUSHE_BREEZE',
            'house_orientation': 'SOURTH',
            'remould_rooms': rooms,
            'remould_livings': livings,
            'remould_kitchens': kitchens,
            'remould_bathrooms': bathrooms,
            'remould_balconys': balconys,
            'info_id': self.info_id,
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
            'project_no': self.project_no,
            'entrust_type': self.entrust_type
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'项目方案制定完成')
            return

    def configList(self):
        """物品清单"""

        def designConfigList():
            """制定物品清单"""

            def getZoneId():
                """获取甲房间的zone_id"""
                url = 'http://decorate.ishangzu.com/isz_decoration/NewConfigurationController/queryZone/%s' % self.project_id
                result = myRequest(url, method='get')
                if result:
                    zoneInfo = result['obj']
                    for i in zoneInfo:
                        if i['function_zone'] == u'甲':
                            zoneId = i['zone_id']
                            return zoneId

            def confirm():
                """制定订单"""
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
                """下单"""
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

        def acceptanceConfigList():
            """物品清单验收"""

            def getSupplierOrderDetail(supplierId):
                """获取物品清单信息"""
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/supplierOrdersDetail'
                data = {"project_id": self.project_id, "supplier_id": supplierId}
                result = myRequest(url, data)
                if result:
                    return result['obj']

            def acceptanceConfirm():
                """验收确认"""
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationConfigController/acceptance/confirm'
                supplierIds = self.config_suppliers
                configsVo = []
                for supplierId in supplierIds:
                    configs = getSupplierOrderDetail(supplierId)
                    for config in configs:
                        configsVo.append(config)
                for i in configsVo:
                    i['real_delivery_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                result = myRequest(url, configsVo)
                if result:
                    consoleLog(u'物品清单验收完成!')
                    return

            acceptanceConfirm()

        designConfigList()
        acceptanceConfigList()

    def stuffList(self):
        """装修清单"""

        commonData = [
            {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "create_uid": self.user.user_id,
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
                "update_uid": self.user.user_id,
                "zone_type": None,
                "type_index": 0,
                "fun_index": 0
            }, {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "create_uid": self.user.user_id,
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
                "update_uid": self.user.user_id,
                "zone_type": None,
                "fun_index": 1,
                "type_index": 1
            }, {
                "acceptance_num": None,
                "acceptance_num_this": 0,
                "acceptance_time": None,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "create_uid": self.user.user_id,
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
                "update_uid": self.user.user_id,
                "zone_type": None,
                "fun_index": 1,
                "type_index": 1
            }
        ]

        def designStuffList():
            """制定装修清单"""

            def preview():
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/preview'
                data = commonData
                result = myRequest(url, data)
                if result:
                    return

            def saveStuffLists():
                preview()
                url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationStuffController/saveStuffLists'
                projectInfo = sqlbase.serach(
                    "select b.address,a.config_order_no,b.contract_id,b.contract_num,b.create_time,b.entrust_end_date,b.entrust_start_date,b.house_code,b.housekeep_mange_uid,b.info_id,"
                    "a.project_no,b.sign_date,b.city_code,b.city_name from %s.decoration_house_info b inner join  %s.new_decoration_project a on a.info_id=b.info_id and a.project_id='%s'" % (
                        get_conf('db', 'decoration_db'), get_conf('db', 'decoration_db'), self.project_id))
                construct_person = UserInfo(self.construct_uid)
                data = {
                    "newStuffList": commonData,
                    "project": {
                        "address": self.address,
                        "build_area": self.build_area,
                        "cable_laying_type": "INNERPIPEINNERLINE",
                        "cable_laying_type_name": None,
                        "city_code": self.city_code,
                        "city_name": self.city_name,
                        "closed_water_test_result": self.closed_water_test_result,
                        "complete_two_nodes": self.complete_two_nodes,
                        "complete_two_nodes_list": self.complete_two_nodes,
                        "config_list_status": self.config_list_status,
                        "config_list_status_name": get_dict_value(self.config_list_status),
                        "config_order_no": self.config_order_no,
                        "config_progress": self.config_progress,
                        "config_progress_name": get_dict_value(self.config_progress),
                        "config_submit_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "config_submit_uid": self.config_submit_uid,
                        "config_submit_uname": self.config_submit_uname,
                        "construct_uid": self.construct_uid,
                        "construct_uname": self.construct_uname,
                        "construct_uname_phone": "%s/%s" % (construct_person.user_name, construct_person.user_phone),
                        "contract_id": self.contract_id,
                        "contract_num": self.contract_num,
                        "contract_type": self.contract_type,
                        "contract_type_name": get_dict_value(self.contract_type),
                        "create_time": self.create_time,
                        "create_uid": self.create_uid,
                        "current_one_node": self.current_one_node,
                        "decoration_style": "WUSHE_BREEZE",
                        "decoration_style_name": "随寓和风",
                        "deleted": 0,
                        "deliver_room_date": "1970-01-02 00:00:00.0",
                        "dispach_remark": "测试",
                        "entrust_end_date": self.entrust_end_date,
                        "entrust_start_date": self.entrust_start_date,
                        "entrust_type_fact": "SHARE",
                        "entrust_type_fact_name": "合租",
                        "grade": 20,
                        "hidden_check_date": "1970-01-02 00:00:00.0",
                        "house_code": self.house_code,
                        "housekeep_mange_name": None,
                        "housekeep_mange_uid": self.housekeep_mange_uid,
                        "info_id": self.info_id,
                        "is_active": "Y",
                        "is_active_name": "是",
                        "one_level_nodes": self.one_level_nodes,
                        "order_status_name": "进程中",
                        "order_type_name": "新收配置订单",
                        "overall_check_date": "1970-01-02 00:00:00.0",
                        "phone": "18815286582",
                        "place_order_date": self.place_order_date,
                        "place_order_dep": "",
                        "place_order_dep_name": None,
                        "place_order_reason": "测试",
                        "place_order_uid": self.user.user_id,
                        "place_order_uname": self.user.user_id,
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

            self.update()
            saveStuffLists()

        def acceptanceStuffList():
            """装修清单验收"""
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

    def hideAndStufCheck(self):
        """施工中"""

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
                IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % attachment['attach_type'])
                attachment['imgs'][0]['url'] = IMG.url
                attachment['imgs'][0]['img_id'] = IMG.id
            result = myRequest(url, data)
            if result:
                consoleLog(u'隐蔽验收完成')
                return

        def stufCheck():
            """硬装验收"""
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
                IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % attachment['attach_type'])
                attachment['imgs'][0]['url'] = IMG.url
                attachment['imgs'][0]['img_id'] = IMG.id
            result = myRequest(url, data)
            if result:
                consoleLog(u'硬装验收完成')
                return

        hideCheck()
        stufCheck()

    def projectCheck(self):
        """项目验收"""

        def wholeCheck():
            """整体验收"""
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/wholeCheck'
            IMG_CARDS = upLoadPhoto(url=self.uploadPhotoURL, filename='CARDS.png')
            IMG_THREE = upLoadPhoto(url=self.uploadPhotoURL, filename='THREE.png')
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

        def profee():
            """物业交割"""
            url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proCheck/profee'
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='PROPERTY_DELIVERY_ORDER.png')
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

        def costSettle():
            """费用结算"""
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

    def indoorImg(self):
        """室内图"""
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/indoor'
        IMG_LAYOUT = upLoadPhoto(url=self.uploadPhotoURL, filename='LAYOUT.png')
        data = {
            "curOneLevelNode": None,
            "curTwoLevelNode": None,
            "deliver_room_date": None,
            "house_attachs": [{
                "attach_type": "PUBLIC_TOILET_1",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 0,
                    "type": "PUBLIC_TOILET_1"
                }]
            }, {
                "attach_type": "KITCHEN_1",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 1,
                    "type": "KITCHEN_1"
                }]
            }, {
                "attach_type": "PARLOUR_1",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 2,
                    "type": "PARLOUR_1"
                }]
            }, {
                "attach_type": "METH",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 3,
                    "type": "METH"
                }]
            }, {
                "attach_type": "ETH",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 4,
                    "type": "ETH"
                }]
            }, {
                "attach_type": "PROP",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 5,
                    "type": "PROP"
                }]
            }, {
                "attach_type": "BALCONY_1",
                "imgs": [{
                    "url": None,
                    "img_id": None,
                    "create_name": "",
                    "create_dept": "",
                    "create_time": "",
                    "sort": 6,
                    "type": "BALCONY_1"
                }]
            }, {
                "attach_type": "BALCONY_2",
                "imgs": [{
                    "url": None,
                    "img_id": None,
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
            IMG = upLoadPhoto(url=self.uploadPhotoURL, filename='%s.png' % house_attach['attach_type'])
            house_attach['imgs'][0]['url'] = IMG.url
            house_attach['imgs'][0]['img_id'] = IMG.id
        result = myRequest(url, data)
        if result:
            # consoleLog(u'室内图添加完成')
            return

    def delivery(self):
        """交房"""
        url = 'http://decorate.ishangzu.com/isz_decoration/NewDecorationProjectController/proComp/delivery'
        data = {
            "deliver_room_date": '%s 10:00:00' % addDays(1),
            "project_id": self.project_id,
            "remark": ""
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'竣工完成')
            return

    def fitment(self):
        """整个装修流程"""
        self.placeOrder()  # 下单
        self.dispatchOrder()  # 派单
        self.acceptOrder()  # 接单
        self.survey()  # 勘测
        self.projectOrder()  # 项目计划
        self.configList()  # 物品清单
        self.stuffList()  # 装修清单
        self.hideAndStufCheck()  # 施工中
        self.projectCheck()  # 项目验收
        self.indoorImg()  # 室内图
        self.delivery()  # 竣工

# -*- coding:utf8 -*-

from isz.houseContract import HouseContract
from common import sqlbase
from common.base import consoleLog
from common.datetimes import addDays, addMonths, addMonthExDay
from common.dict import free_date_par, landlord, getUserInfo
from isz.contractBase import ContractBase
from isz.infoClass import HouseInfo


class House(HouseInfo):
    """业主房源信息"""

    # 新签委托合同
    def createHouseContract(self, contract_num, apartment_type, entrust_type, sign_date, owner_sign_date, entrust_start_date,
                         entrust_year, rent, parking=None, payment_cycle='HALF_YEAR',fitment_start_date=None, fitment_end_date=None,
                         contract_type='NEWSIGN'):
        """
        新增委托合同以及分割交房之后同时定价
        :param apartment_type: 公寓类型
        :param entrust_type: 合同类型
        :param sign_date: 签约日期
        :param owner_sign_date: 业主交房日
        :param entrust_start_date: 委托起算日
        :param rent: 房租
        :param parking:车位费
        :param payment_cycle:付款类型
        :param fitment_start_date:装修起算日，默认无
        :param fitment_end_date:装修结束日，默认无
        :param contract_type:合同类型，默认新签
        :return:合租返回其中一条公寓ID，整租直接返回公寓ID
        """

        contractbase = ContractBase()
        signUser = getUserInfo()
        signUser = {
            'sign_user_name': signUser['user_name'],
            'sign_uid': signUser['uid'],
            'sign_dep_name': signUser['dep_name'],
            'sign_did': signUser['did']
        }
        landlordInfo = landlord
        sign_date = sign_date
        owner_sign_date = owner_sign_date
        entrust_start_date = entrust_start_date
        entrust_year_after = addDays(-1, addMonths(12 * entrust_year, entrust_start_date))
        entrust_end_date = addDays(free_date_par[payment_cycle] * entrust_year, entrust_year_after)
        delay_date = entrust_end_date
        # 免租期 （默认首月）
        # free_start_date = entrust_start_date if freeType == 'STARTMONTH' else free_start_date
        # free_end_date = addDays(-1, addMonths(1, entrust_start_date)) if freeType == 'STARTMONTH' else free_end_date
        # 付款日 默认委托下个月30号为第一次，
        first_pay_date = addMonthExDay(30, months=0, date=entrust_start_date)
        second_pay_date = addMonthExDay(30, months=2, date=entrust_start_date)
        # 装修期 品牌默认签约前一个月 托管默认无
        fitment_start_date = addMonths(-1,
                                       entrust_start_date) if fitment_start_date is None else fitment_start_date
        fitment_end_date = addDays(-1,
                                   entrust_start_date) if fitment_end_date is None else fitment_end_date

        houseContractFirst = {
            'address': self.property_name,
            'certificate_type': '',
            'certificate_type_id': '2',  # 产权证类型 （默认房屋所有权）
            'commonLandlords': [],
            'common_case': 'PRIVATE',  # 共有情况 （默认私有）
            'common_case_cn': '',
            'contract_id': None,
            'contract_type': contract_type,
            'contract_type_cn': u'新签' if contract_type == 'NEWSIGN' else u'续签',
            'houseContractLandlord': {
                'card_type': landlordInfo['card_type'],  # 产权人证件类型 （默认护照）
                'id_card': landlordInfo['id_card'],  # 证件号 （默认）
                'landlord_name': landlordInfo['landlord_name'],  # 产权人姓名 （默认）
                'property_owner_type': 'PROPERTYOWNER',  # 产权人类型 （默认个人）
                'property_card_id': 'chanquanzheng',  # 产权证号 （默认）
                'idCardPhotos': [{
                    'src': 'http://img.ishangzu.com/erp/2018/2/9/15/ceec21bc-c6e5-481a-92cf-21a1d7982b12.jpg',  # 默认
                    'url': 'http://img.ishangzu.com/erp/2018/2/9/15/ceec21bc-c6e5-481a-92cf-21a1d7982b12.jpg',  # 默认
                    'remark': '',
                    'img_id': 'FF80808161C581A90161C5A7893B0010'  # 默认
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/15/c30e57ce-f24a-4334-bc68-a0acea61fa4b.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/15/c30e57ce-f24a-4334-bc68-a0acea61fa4b.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162852842010265"
                }]  # 证件照片
            },  # 产权人信息
            'house_code': self.house_code,  # 房源code
            'inside_space': self.build_area if self.build_area else '120.00',  # 使用面积 默认收房面积
            'is_new_data': None,
            'mortgageeStatementOriginal': [],
            'pledge': '0',
            'productionVos': [{
                "attachments": [{
                    "src": "http://img.ishangzu.com/erp/2018/3/30/10/d735a299-cb64-4298-aad8-c65f0e5b6147.png",
                    "url": "http://img.ishangzu.com/erp/2018/3/30/10/d735a299-cb64-4298-aad8-c65f0e5b6147.png",
                    "remark": "",
                    "img_id": "FF808081626BF853016274D8BB3F0462"
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/14/ac70ffd5-5397-41e8-a40a-2f2f41ec6d5b.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/14/ac70ffd5-5397-41e8-a40a-2f2f41ec6d5b.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162850B52960257"
                }],
                "file_type": "主页（业主姓名/物业地址）",
                "file_type_id": contractbase.getFileTypeId("主页(有业主姓名/物业地址页)"),
                "is_active": "Y",
                "is_approved_need": "N",
                "is_audit_need": "Y",
                "is_save_need": "Y"
            }, {
                "attachments": [{
                    "src": "http://img.ishangzu.com/erp/2018/3/30/10/28e31cff-3aeb-481a-ade6-af643efae25b.png",
                    "url": "http://img.ishangzu.com/erp/2018/3/30/10/28e31cff-3aeb-481a-ade6-af643efae25b.png",
                    "remark": "",
                    "img_id": "FF808081626BF853016274D8C1D70463"
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/14/47d8d465-1f91-43ff-b835-7d50aa5a1b76.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/14/47d8d465-1f91-43ff-b835-7d50aa5a1b76.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162850F184C0260"
                }],
                "file_type": "带证号页(产权证编号)",
                "file_type_id": contractbase.getFileTypeId("带证号页(有产权证编号页)"),
                "is_active": "Y",
                "is_approved_need": "N",
                "is_audit_need": "N",
                "is_save_need": "Y"
            }, {
                "attachments": [{
                    "src": "http://img.ishangzu.com/erp/2018/3/30/10/bda51090-8294-4675-ba85-cbd1f19f600a.png",
                    "url": "http://img.ishangzu.com/erp/2018/3/30/10/bda51090-8294-4675-ba85-cbd1f19f600a.png",
                    "remark": "",
                    "img_id": "FF808081626BF853016274D8FB1E0466"
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/14/05ece962-549e-4005-858c-3e89c1636edf.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/14/05ece962-549e-4005-858c-3e89c1636edf.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162850F2BE30262"
                }],
                "file_type": "附记页",
                "file_type_id": contractbase.getFileTypeId("附记页"),
                "is_active": "Y",
                "is_approved_need": "N",
                "is_audit_need": "N",
                "is_save_need": "Y"
            }, {
                "attachments": [{
                    "src": "http://img.ishangzu.com/erp/2018/3/30/10/6aacb6a1-94e2-42c4-aeef-c712d3ac677d.png",
                    "url": "http://img.ishangzu.com/erp/2018/3/30/10/6aacb6a1-94e2-42c4-aeef-c712d3ac677d.png",
                    "remark": "",
                    "img_id": "FF808081626BF853016274D8E4FE0465"
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/14/695674d7-b45c-45d1-8699-f0700bff5931.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/14/695674d7-b45c-45d1-8699-f0700bff5931.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162850EEA88025E"
                }],
                "file_type": "分户图",
                "file_type_id": contractbase.getFileTypeId("分户图"),
                "is_active": "Y",
                "is_approved_need": "N",
                "is_audit_need": "N",
                "is_save_need": "N"
            }, {
                "attachments": [{
                    "src": "http://img.ishangzu.com/erp/2018/3/30/11/fdc19823-e59d-400a-bc5a-b44729fed558.png",
                    "url": "http://img.ishangzu.com/erp/2018/3/30/11/fdc19823-e59d-400a-bc5a-b44729fed558.png",
                    "remark": "",
                    "img_id": "FF808081626BF853016274D9048B0467"
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/14/7c57a909-940a-4c3b-926a-05bb03e85ecc.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/14/7c57a909-940a-4c3b-926a-05bb03e85ecc.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162850EFC5E025F"
                }],
                "file_type": "原户型图",
                "file_type_id": contractbase.getFileTypeId("原户型图"),
                "is_active": "Y",
                "is_approved_need": "N",
                "is_audit_need": "N",
                "is_save_need": "N"
            }, {
                "attachments": [{
                    "src": "http://img.ishangzu.com/erp/2018/3/30/11/a9b3ae6b-cf79-4026-af07-29cb7f0f6748.png",
                    "url": "http://img.ishangzu.com/erp/2018/3/30/11/a9b3ae6b-cf79-4026-af07-29cb7f0f6748.png",
                    "remark": "",
                    "img_id": "FF808081626BF853016274D90EA90468"
                }, {
                    "src": "http://img.ishangzu.com/erp/2018/4/2/14/36e5c1cd-b624-4c6b-9d2a-eec2176272fa.png",
                    "url": "http://img.ishangzu.com/erp/2018/4/2/14/36e5c1cd-b624-4c6b-9d2a-eec2176272fa.png",
                    "remark": "",
                    "img_id": "FF80808162756A8E0162850EDB0C025D"
                }],
                "file_type": "其他",
                "file_type_id": contractbase.getFileTypeId("其他"),
                "is_active": "Y",
                "is_approved_need": "N",
                "is_audit_need": "N",
                "is_save_need": "N"
            }],  # 产证资料 （默认产权类型为房屋所有权格式）
            'production_address': self.property_name,  # 产权地址
            'property_card_id': None,
            'property_use': 'HOUSE',  # 物业用途 （默认住宅）
            'property_use_cn': ''
        }  # 房源信息（选择不同的产权类型可以获取不同格式的产证资料）

        houseContractSecond = {
            'agreedRentOriginalStatements': [],
            'any_agent': '0',  # 有无代理人 （默认无代理人）
            'assetsOfLessor': [{
                'landlord_name': landlordInfo['landlord_name'],
                'phone': landlordInfo['phone'],
                'email': landlordInfo['email'],
                'mailing_address': landlordInfo['mailing_address']
            }],  # 资产出租人
            'contract_id': None,
            'houseContractSign': {
                'address': '',
                'agent_type': '',
                'attachments': [],
                'card_type': '',
                'email': '',
                'id_card': '',
                'phone': '',
                'sign_name': ''
            },
            'is_new_data': None,
            'originalAgentDataRelations': [],
            'originalLessorHasDied': []
        }  # 出租人

        houseContractThird = {
            'account_bank': u'海创支行',  # 收款行支行（默认）
            'account_name': landlordInfo['landlord_name'],  # 收款人姓名
            'account_num': '6123465789132',  # 收款账号 （默认）
            'bank': u'未知发卡银行',  # 收款银行 （默认）
            'contract_id': None,
            'is_new_data': None,
            'notPropertyOwnerGrantReceipts': [],
            'pay_object': 'PERSONAL',  # 收款账号类型 （默认个人）
            'payeeIdPhotos': [{
                'src': 'http://img.ishangzu.com/erp/2018/2/9/15/ceec21bc-c6e5-481a-92cf-21a1d7982b12.jpg',  # 默认
                'url': 'http://img.ishangzu.com/erp/2018/2/9/15/ceec21bc-c6e5-481a-92cf-21a1d7982b12.jpg',  # 默认
                'remark': '',
                'img_id': 'FF808081616A30FA01617968993804B0'  # 默认
            }, {
                'src': 'http://img.ishangzu.com/erp/2018/2/24/10/12c0c38a-56c4-431c-9589-fd4029013f28.jpg',  # 默认
                'url': 'http://img.ishangzu.com/erp/2018/2/24/10/12c0c38a-56c4-431c-9589-fd4029013f28.jpg',  # 默认
                'remark': '',
                'img_id': 'FF80808161C581A90161C5A7893B0010'  # 默认
            }],  # 证件照片
            'payee_card_type': landlordInfo['card_type'],  # 证件类型
            'payee_card_type_cn': '',
            'payee_emergency_name': u'紧急',  # 紧急人姓名（默认）
            'payee_emergency_phone': '13600000000',  # 紧急人手机号码（默认）
            'payee_id_card': landlordInfo['id_card'],  # 证件号
            'payee_type': 'PROPERTYOWNER',  # 收款人类型 （默认产权人）
            'payee_type_cn': ''
        }  # 收款人&紧急联系人

        rentStrategysData = {
            "apartment_type": apartment_type,
            "contract_type": "NEWSIGN",
            "entrust_start_date": entrust_start_date,
            "entrust_end_date": entrust_end_date,
            "free_end_date": "",
            "free_start_date": "",
            "parking": "",
            "payment_cycle": payment_cycle,
            "rent_money": str(rent),
            "sign_date": sign_date,
            "city_code": self.city_code,
            "entrust_year": entrust_year,
            "free_days": free_date_par[payment_cycle],
            "version": "V_THREE"}  # 传到合同信息中

        rentStrategys = contractbase.getRentStrategys(rentStrategysData)  # 租金策略

        houseContractFour = {
            'apartment_type': apartment_type,  # 公寓类型
            'apartment_type_cn': '',
            'area_code': self.area_code,  # 城区
            'audit_status': None,
            'audit_time': None,
            'audit_uid': None,
            'building_id': self.building_id,
            'city_code': self.city_code,  # 城市
            'contractAttachments': [{
                "src": "http://image.ishangzu.com/erp/2018/3/30/13/51d1a715-ada2-4d71-921e-d061aed71c6d.png",
                "url": "http://image.ishangzu.com/erp/2018/3/30/13/51d1a715-ada2-4d71-921e-d061aed71c6d.png",
                "img_id": "FF808081626BF8530162756F164B04DE"
            }, {
                "src": "http://img.ishangzu.com/erp/2018/4/2/14/ec255478-78fe-44de-bb96-210d01d96e69.png",
                "url": "http://img.ishangzu.com/erp/2018/4/2/14/ec255478-78fe-44de-bb96-210d01d96e69.png",
                "img_id": "FF80808162756A8E01628514ED670263"
            }],
            'contract_id': None,
            'contract_num': contract_num,
            'contract_status': None,
            'contract_type': contract_type,
            'contract_type_cn': u'新签' if contract_type == 'NEWSIGN' else u'续签',
            'delay_date': delay_date,  # 延长到期日
            "free_days": free_date_par[payment_cycle],
            'electron_file_src': None,
            'energy_company': None,
            "entrust_year": entrust_year,
            "entrust_year_cn": "",
            'energy_fee': None,
            'entrust_end_date': entrust_end_date,  # 委托到期日
            'entrust_start_date': entrust_start_date,  # 委托开始日期
            'entrust_type': entrust_type,  # 合同类型
            'entrust_type_cn': '',
            'first_pay_date': first_pay_date,  # 首次付款日
            'fitment_end_date': fitment_end_date,  # 装修到期日
            'fitment_start_date': fitment_start_date,  # 装修起算日
            'freeType_cn': '',
            'have_parking': 'Y',  # 是否有停车位 （默认有）
            'house_id': self.house_id,
            'housekeep_mange_dep': None,
            'housekeep_mange_dep_user': '-',
            'housekeep_mange_did': None,
            'housekeep_mange_uid': None,
            'housekeep_mange_user_name': None,
            'is_electron': None,
            'is_new_data': None,
            'owner_sign_date': owner_sign_date,  # 签约日期
            'parent_id': None,
            'parking': str(parking),  # 车位费（默认）
            'payment_cycle': payment_cycle,  # 付款方式
            'payment_cycle_cn': '',
            'property': None,
            'property_company': None,
            'reform_way': 'OLDRESTYLE' if apartment_type is 'BRAND' else 'TINYCHANGE',  # 改造方式RESTYLED
            'reform_way_cn': '',
            'remark': None,
            'rentMoney': str(rent),  # 租金
            'rentStrategys': rentStrategys,
            'rental_price': str(float(rent) + float(parking)),  # 总租金
            'reset_finance': 'false',
            'residential_id': self.residential_id,
            'second_pay_date': second_pay_date,  # 第二次付款日
            'server_manage_dep_user': '',
            'server_manage_did': None,
            'server_manage_did_name': None,
            'server_manage_uid': None,
            'server_manage_uid_name': None,
            'service_fee_factor': 0.01,  # 年服务费 （默认）
            'sign_body': 'ISZPRO',  # 签约公司 （默认）
            'sign_date': sign_date,
            'sign_dep_name': signUser['sign_dep_name'],  # 签约部门
            'sign_did': signUser['sign_did'],
            'sign_uid': signUser['sign_uid'],
            'sign_user_name': signUser['sign_user_name'],  # 签约人
            'year_service_fee': None
        }  # 合同信息

        contractPayableData = {
            'contractId': None,
            'firstPayDate': first_pay_date,
            'secondPayDate': second_pay_date,
            'rentInfoList': rentStrategys,
            'version': 'V_THREE'
        }

        houseContractFive = contractbase.createContractPayable(contractPayableData)  # 服务费&应付

        houseContract = {
            'houseContractFrist': houseContractFirst,
             'houseContractSecond': houseContractSecond,
             'houseContractThird': houseContractThird,
             'houseContractFour': houseContractFour,
             'houseContractFive': houseContractFive
        }

        result = contractbase.saveHouseContract(houseContract)
        if result:
            houseContractInfo = sqlbase.serach(
                "select contract_id,contract_num,house_id from house_contract where house_id = '%s' and deleted = 0 order by create_time desc limit 1" %
                self.house_id)
            consoleLog(u'新签委托合同成功！')
            consoleLog(u'合同编号 : %s 合同ID : %s' % (houseContractInfo[1], houseContractInfo[0]))
            return HouseContract(houseContractInfo[0])


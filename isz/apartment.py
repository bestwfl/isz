# -*- coding:utf8 -*-
import time
from isz.apartmentContract import ApartmentContract
from common import sqlbase
from common.base import consoleLog, get_conf, solr, get_randomString
from common.dict import userInfo, ROOM_NAME
from common.interface_wfl import myRequest, delNull
from isz.infoClass import ApartmentInfo


class Apartment(ApartmentInfo):
    """房源相关"""

    @staticmethod   # 跟进room_id获取房间号
    def roomName(room_id):
        if not (room_id is None or room_id == 'None'):
            room_no = sqlbase.serach("select room_no from house_room where room_id='%s'" % room_id)[0]
            return ROOM_NAME[room_no]
        else:
            return None

    # 定价
    def confirmPrice(self, house_rent_price):
        # houseInfo = self.houseInfo()
        if self.rent_type == 'SHARE':
            url = 'isz_house/ApartmentController/searchShareApartment.action'
            # apartments_id = sqlbase.serach("SELECT apartment_id from apartment where house_id = '%s'  and rent_type='SHARE'" % houseInfo['houseID'], oneCount=False)
            requestPayload = {
                'apartment_id': self.apartment_id
            }
            result = myRequest(url, requestPayload)
            if result:
                url = 'isz_house/ApartmentController/confirmPricing.action'
                requestPayload = []
                # 根据房间数量，动态将参数添加至定价请求参数中
                default_rent_price = 1000
                x = 0
                for content in result['obj']:
                    # content = result['obj'][x]
                    if 'func_type_desc' in content:
                        del content['func_type_desc']
                    if 'rent_price' in content:
                        del content['rent_price']
                    if x is 0:
                        content['current_apartment'] = 'Y'
                    x = x + 1
                    # default_rent_price += 0.01
                    content['rent_price'] = str(house_rent_price) if house_rent_price else str(default_rent_price)
                    requestPayload.append(content)
                result = myRequest(url, requestPayload)
                if result:
                    # 避免等待时间太长，生成的房源没有出来，此处调用solr的增量操作
                    solr('apartment', get_conf('testCondition', 'test'))
                    consoleLog(u'房源 %s 完成定价' % self.house_code)
                    self.rent_price = house_rent_price
                    return self.apartment_id
        else:
            url = 'isz_house/ApartmentController/confirmApatmentRentPricing.action'
            # for i in range(10):
            #     apartments_id = sqlbase.serach(
            #         "SELECT apartment_id from apartment where house_id = '%s' and date(create_time)=date(sysdate())" %
            #         self.house_id)
            #     if apartments_id:
            #         break
            #     else:
            #         time.sleep(1)
            requestPayload = {
                'apartment_id': self.apartment_id,
                'rent_price': str(house_rent_price) if house_rent_price else '2000'
            }
            result = myRequest(url, requestPayload)
            if result:
                # 避免等待时间太长，生成的房源没有出来，此处调用solr的增量操作
                # solr('apartment', get_conf('testCondition', 'test'))
                consoleLog(u'房源 %s 完成定价' % self.house_code)
                self.rent_price = house_rent_price
                return self.apartment_id

    # 修改定价
    def modifiApartmentRentPrice(self, rentPrice):
        url = 'isz_house/ApartmentController/confirmApatmentRentPricing.action'
        data = {
            'apartment_id': self.apartment_id,
            'rent_price': str(rentPrice)
        }
        myRequest(url, data)

    # 更新成本占比
    def updateCostAccount(self, rentPrice):
        url = 'isz_house/ApartmentController/updateCostAccount.action'
        data = {'apartment_id': self.apartment_id, 'rent_price': str(rentPrice)}
        myRequest(url, data)

    # 检查上架信息完整
    def __cheackOnlineHouse(self):
        url = "/isz_house/onlineHouseController/checkOnlineHouseNew.action"
        data = {
            "apartment_id": self.apartment_id,
            "rent_type": self.rent_type
        }
        result = myRequest(url, data)
        if result['obj']['flag']:
            consoleLog(u'房源上架信息校验通过')
            return
        else:
            consoleLog(u'房源上架信息未完善')

    # 整租房源上架信息
    def selectApartmentDetail(self):
        url = '/isz_house/ApartmentController/selectApartmentDetail.action'
        data = {
            "apartment_id": self.apartment_id
        }
        result = myRequest(url, data)
        if result:
            return result['obj']

    # 合租房源上架信息
    def selectShareHouseDetail(self):
        url = '/isz_house/ApartmentController/selectShareHouseDetail.action'
        data = {
            "apartment_id": self.apartment_id
        }
        result = myRequest(url, data)
        if result:
            return result['obj']

    # 保存申请图片(整租)
    def __saveHouseImage(self):
        houseImgList = self.selectApartmentDetail()['houseImgList']
        houseImgListNew = []
        if houseImgList:
            i = 0
            for houseImg in houseImgList:
                i = i + 1
                houseImgNew = {
                    "audit_status": houseImg['audit_status'],
                    "building_id": houseImg['building_id'],
                    "create_dep": houseImg['create_dep'],
                    "create_time": houseImg['create_time'],
                    "create_uid": houseImg['create_uid'],
                    "create_user": houseImg['create_user'],
                    "deleted": 0,
                    "house_id": houseImg['house_id'],
                    "house_img_id": houseImg['house_img_id'],
                    "img_id": houseImg['img_id'],
                    "img_type": houseImg['img_type'],
                    "residential_id": houseImg['residential_id'],
                    "sort": i,
                    "src": houseImg['src']
                }
                houseImgListNew.append(houseImgNew)
        else:
            for j in range(3):
                houseImgNew = {
                    "audit_status": "NO_AUDIT",
                    "building_id": self.building_id,
                    "create_dep": userInfo['dep_name'],
                    "create_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "create_uid": userInfo['uid'],
                    "create_user": userInfo['user_name'],
                    "deleted": 0,
                    "house_id": self.house_id,
                    "house_img_id": houseImgList['house_img_id'],
                    "img_id": houseImgList['img_id'],
                    "img_type": "INDOOR_IMGS",
                    "residential_id": self.residential_id,
                    "sort": j + 1,
                    "src": houseImgList['src']
                }
                houseImgListNew.append(houseImgNew)
        url = "/isz_house/ApartmentController/saveHouseImage.action"
        data = {
            "houseImgList": houseImgList,
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "apartment_id": self.apartment_id
        }
        result = myRequest(url, data)
        if result:
            return

    # 上架申请
    def houseOnline(self):
        self.__cheackOnlineHouse()
        self.__saveHouseImage()
        url = "/isz_house/onlineHouseController/saveOnlineHouseInfoNew.action"
        data = {
            "door_model_describing": u'测试描述：测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述',
            "position_description": u'测试描述：测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述',
            "agent_description": u'测试描述：测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述',
            "apartment_id": self.apartment_id,
            "house_id": self.house_id,
            "rent_type": self.rent_type,
            "house_description": u'测试描述：测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述',
            "plot_describing": u'测试描述：测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述',
            "manager_description": u'测试描述：测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述测试描述'
        }
        result = myRequest(url, data)
        if result:
            consoleLog(u'房源上架申请完成')
            return

    # 上架审核
    def onlineAudit(self):
        url = ""
        data = {}

    # 新增出租合同
    def createApartmentContract(self, customerInfo, rent_price, sign_date,
                                rent_start_date, rent_end_date, payment_cycle,
                                contract_num=None, sign_phone=None, sign_name=None,
                                sign_id_type=None, sign_id_no=None):
        """
        新增出租合同
        :param sign_id_no: 签约人证件号
        :param sign_id_type: 签约人证件类型
        :param sign_name: 签约人姓名
        :param sign_phone: 签约人手机号
        :param contract_num: 合同号，可以为空，默认随机生成
        :param customerInfo: 签约的租前客户信息，创建租客的接口会返回此信息
        :param rent_price: 目标出租价格（由于半年付和年付会有优惠，此价格直接为优惠后的价格）
        :param sign_date: 签约日期
        :param rent_start_date: 承租起算日
        :param rent_end_date: 承租到期日
        :param payment_cycle:付款周期

        :return: 返回创建的合同信息字典
        """

        # 如果房源未定价则现将房源定价，定价金额为租金金额
        if self.rent_price is None or self.rent_price == 0 or self.rent_price == 'None':
            self.confirmPrice(rent_price)  # 定价
        deposit = rent_price = float(self.rent_price)
        sign_name = u'签约人' if not sign_name else sign_name
        sign_phone = '13600000000' if not sign_phone else sign_phone
        sign_id_type = 'PASSPORT' if not sign_id_type else sign_id_type
        sign_id_no = 'huzhao123' if not sign_id_no else sign_id_no
        if payment_cycle is 'HALF_YEAR':  # 付款周期和租金规则
            real_due_rent_price = rent_price * 0.985
        elif payment_cycle is 'ONE_YEAR':
            real_due_rent_price = rent_price * 0.97
        else:
            real_due_rent_price = rent_price
        # 随机生成出租合同号
        contract_num = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S') + get_randomString(2) if not contract_num else contract_num
        data = {
            'contract_num': contract_num,  # 合同编号
            'sign_date': sign_date,  # 签约日期
            'rent_start_date': rent_start_date,  # 承租起算日
            'rent_end_date': rent_end_date,  # 承租结束日
            'payment_date': rent_start_date,  # 首次付款日
            'deposit': str(deposit),  # 押金
            'payment_type': 'NORMAL',  # 付款方式
            'payment_cycle': payment_cycle,  # 付款周期
            'cash_rent': str(rent_price * 0.1),  # 转租费
            'agency_fee': '1000',  # 中介服务费
            'month_server_fee_discount': '100%',  # 服务费折扣
            'remark': 'remark',  # 备注
            'sign_name': sign_name,  # 签约人
            'sign_id_type': sign_id_type,  # 签约人证件类型
            'sign_id_no': sign_id_no,  # 签约人证件号
            'sign_phone': sign_phone,  # 签约人手机号
            'sign_is_customer': 'Y',  # 签约人是否是承租人
            'postal_address': u'通讯地址',  # 签约人通讯地址
            'deposit_type': 'ONE',
            'depositIn': '1',
            'apartmentContractRentInfoList': [
                {
                    'firstRow': True,
                    'money': str(real_due_rent_price),
                    'start_date': rent_start_date,
                    'end_date': rent_end_date,
                    'rowIndex': 0,
                    'money_cycle': payment_cycle,
                    'payment_date': rent_start_date,
                    'deposit': deposit,
                    'agencyFeeMoney': 1000,
                    'money_type': 'RENT',
                    'rent_start_date': rent_start_date,
                    'rent_end_date': rent_end_date,
                    'sign_date': sign_date
                }
            ],
            'person': {
                "urgent_customer_name": "紧急联系人",
                "urgent_phone": "13600000001",
                "urgent_card_type": "PASSPORT",
                "urgent_id_card": "huzhaohuzhao",
                "urgent_postal_address": "紧急联系人通讯地址",
                "customer_id": customerInfo['customer_id'],  # FF8080815F0A26E8015F1427B6040140
                "birth_date": "1992-3-2",
                "constellation": "VIRGO",
                "customer_num": customerInfo['customer_num'],
                "customer_from": "FLOOR19",
                "customer_type": "PERSONALITY",
                "customer_name": sign_name,
                "card_type": sign_id_type,
                "id_card": sign_id_no,
                "phone": sign_phone,
                "gender": "MALE",
                "education": "BACHELOR",
                "trade": "IT",
                "email": "isz@mail.com",
                "tent_contact_address": "通讯地址",
                "yesNo": "Y",
                "person_type": 3
            },
            'persons': [
                {
                    "person_type": 3,
                    "gender": "MALE",
                    "card_type": sign_id_type,
                    "customer_name": sign_name,
                    "id_card": sign_id_no,
                    "phone": sign_phone,
                    "cardType": "护照",
                    "sex": "男",
                    "staydate": time.strftime('%Y-%m-%d')
                }
            ],
            'model': '4'
        }

        # 获取出租合同基础信息
        def searchApartmentContractDetail():
            url = 'isz_contract/ApartmentContractController/searchApartmentContractDetail.action'
            requestPayload = {
                "apartment_id": self.apartment_id,
                "contract_type": "NEWSIGN"
            }
            result = myRequest(url, requestPayload)
            if result:
                content = delNull(result['obj']['apartmentContract'])
                for x, y in content.items():
                    data[x] = y

        # 获取自营房源信息
        def getHouseContractByHouseId(request=myRequest):
            url = 'isz_contract/ApartmentContractController/getHouseContractByHouseId.action'
            requestPayload = {
                "rent_start_date": rent_start_date,
                "rent_end_date": rent_end_date,
                "houseId": self.house_id,
                "apartment_id": self.apartment_id,
                "room_id": self.room_id
            }
            if self.rent_type == 'ENTIRE':
                del requestPayload['room_id']
            result = request(url, requestPayload, shutdownFlag=True)
            if result:
                data['houseContractList'] = delNull(result['obj'])

        #
        def getServiceAgencyProperty():
            url = 'isz_contract/ApartmentContractController/getServiceAgencyProperty.action'
            requestPayload = {
                "houseContractId": self.house_contract_id,  # data['houseContractList'][0]['contract_id'],
                "firstMoney": str(real_due_rent_price),
                "rent_start_date": rent_start_date,
                "rent_end_date": rent_end_date,
                "contract_type": "NEWSIGN",
                "sign_date": sign_date,
                "house_id": self.house_id,
                "room_id": self.room_id
            }
            if self.rent_type == 'ENTIRE':
                del requestPayload['room_id']
            result = myRequest(url, requestPayload)
            if result:
                data['month_server_fee'] = str(result['obj']['month_server_fee'])

        # 生成出租应收
        def createApartmentContractReceivable():
            url = 'isz_contract/ApartmentContractController/createApartmentContractReceivable.action'
            requestPayload = data['apartmentContractRentInfoList']
            result = myRequest(url, requestPayload)
            if result:
                data['receivables'] = delNull(result['obj'])
                index = 0
                for x in data['receivables']:
                    x['edit'] = False
                    x['rowIndex'] = index
                    index += 1

        searchApartmentContractDetail()
        getHouseContractByHouseId()
        getServiceAgencyProperty()
        createApartmentContractReceivable()

        url = 'isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action'
        result = myRequest(url, data, shutdownFlag=True)  # 生成出租合同
        if result:
            consoleLog('承租合同 %s 已创建完成' % data['contract_num'])
            return ApartmentContract(result['par']['contract_id'])

    # 添加保修订单
    def create_repair_order(self):
        pass

if __name__ == '__main__':
    apartment_id = 'SJZ1001168-01'
    apartment = ApartmentInfo(apartment_id)
    print(apartment)

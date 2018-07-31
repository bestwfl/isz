# -*- coding:utf8 -*-
"""表元素基础信息类"""
import threading

# from common import sqlbase
from common import sqlbase
from common.base import consoleLog, get_conf
from common.mysql import Mysql


class HouseInfo(object):
    def __init__(self, houseIdOrCode):
        houseId = Mysql().getOne("select house_id from house where (house_id='%s' or house_code like '%s%s') "
                                 "and deleted=0 " % (houseIdOrCode, houseIdOrCode, '%'))
        if 1 != len(houseId):
            raise ValueError('the house_code is not one but: %s! search for:%s' % (len(houseId), houseIdOrCode))
        sql = "select * from house where house_id='%s' and deleted=0" % houseId[0]
        self.house_info = Mysql().query(sql)[0]
        self.house_id = self.house_info['house_id']
        self.residential_id = self.house_info['residential_id']
        self.building_id = self.house_info['building_id']
        self.city_code = self.house_info['city_code']
        self.area_code = self.house_info['area_code']
        self.house_code = self.house_info['house_code']
        self.unit_id = self.house_info['unit_id']
        self.unit = self.house_info['unit']
        self.floor_id = self.house_info['floor_id']
        self.floor = self.house_info['floor']
        self.house_no_id = self.house_info['house_no_id']
        self.house_no = self.house_info['house_no']
        self.property_name = self.house_info['property_name']
        self.right_num = self.house_info['right_num']  # 产权证号
        self.build_area = self.house_info['build_area']
        self.orientation = self.house_info['orientation']  # 朝向
        self.property_type = self.house_info['property_type']  # 物业类型
        self.property_use = self.house_info['property_use']  # 物业用途
        self.property_right = self.house_info['property_right']  # 物业熟悉


class HouseContractInfo(HouseInfo):
    def __init__(self, contractIdOrNum):
        contractId = Mysql().getAll("select contract_id,house_id from house_contract where (contract_id='%s' or "
                                    "contract_num='%s') and deleted=0" % (contractIdOrNum, contractIdOrNum),
                                    nullLog=False)
        if 1 != len(contractId):
            raise ValueError('the contract_num is not one but: %s! search for:%s' % (len(contractId), contractIdOrNum))
        sql = "select * from house_contract where contract_id='%s' and deleted=0" % contractId[0][0]
        super(HouseContractInfo, self).__init__(contractId[0][1])
        self.house_contract_info = Mysql().query(sql)[0]
        self.house_contract_id = self.house_contract_info['contract_id']
        threading.Thread(target=check_query_table, args=(self.house_contract_id, 'house_contract')).start()
        self.reform_way = self.house_contract_info['reform_way']
        self.is_active = self.house_contract_info['is_active']
        if 'N' == self.is_active:
            consoleLog(u'委托合同非有效')
        self.house_contract_num = self.house_contract_info['contract_num']
        self.apartment_type = self.house_contract_info['apartment_type']
        self.contract_type = self.house_contract_info['contract_type']
        self.entrust_type = self.house_contract_info['entrust_type']
        self.sign_date = self.house_contract_info['sign_date']
        self.sign_body = self.house_contract_info['sign_body']
        self.property_type = self.house_contract_info['property_type']
        self.entrust_start_date = self.house_contract_info['entrust_start_date']
        self.entrust_end_date = self.house_contract_info['entrust_end_date']
        self.payment_cycle = self.house_contract_info['payment_cycle']
        self.first_pay_date = self.house_contract_info['first_pay_date']
        self.house_contract_audit_status = self.house_contract_info['audit_status']
        self.__audit_status = self.house_contract_info['audit_status']
        self.account_name = self.house_contract_info['account_name']
        self.account_bank = self.house_contract_info['account_bank']
        self.account_num = self.house_contract_info['account_num']
        self.fitment_start_date = self.house_contract_info['fitment_start_date']
        self.fitment_end_date = self.house_contract_info['fitment_end_date']
        self.rental_price = self.house_contract_info['rental_price']
        self.real_due_date = self.house_contract_info['real_due_date']
        self.freeType = self.house_contract_info['freeType']
        self.contract_status = self.house_contract_info['contract_status']
        self.production_address = self.house_contract_info['production_address']
        self.pledge = self.house_contract_info['pledge']
        self.owner_sign_date = self.house_contract_info['owner_sign_date']
        self.pay_object = self.house_contract_info['pay_object']
        self.bank = self.house_contract_info['bank']
        self.payee_type = self.house_contract_info['payee_type']
        self.payee_card_type = self.house_contract_info['payee_card_type']
        self.payee_id_card = self.house_contract_info['payee_id_card']
        self.certificate_type_id = self.house_contract_info['certificate_type_id']  # 产权证类型id
        self.common_case = self.house_contract_info['common_case']
        self.any_agent = self.house_contract_info['any_agent']
        self.entrust_year = self.house_contract_info['entrust_year']
        self.free_days = self.house_contract_info['free_days']

    @property
    def audit_status_now(self):
        """ 委托合同实时审核状态"""
        self.__audit_status = Mysql().getOne("select audit_status from house_contract where contract_id='%s' "
                                             "and deleted=0" % self.house_contract_id)[0]
        return self.__audit_status

    def payables(self, audit_status='NOTAUDIT', money_type='RENT'):
        """ 委托合同应付，默认读取未审核的应付租金
        :return 应付ID的集合
        """
        payablesVo = []
        sql = "select * from house_contract_payable where contract_id='%s' and deleted=0" % self.house_contract_id
        payables = Mysql().query(sql)
        for payable in payables:
            payableVo = Payable(payable['payable_id'])
            if not audit_status or audit_status == payableVo.audit_status:
                if not money_type or money_type == payableVo.money_type:
                    payablesVo.append(payableVo)
        return payablesVo

    def step_status(self, step):
        """委托合同分步审核状态"""
        step_status = Mysql().getOne("select status from house_contract_step_audit_status where contract_id = '%s' and "
                                     "step = '%s' and deleted=0 order by step_id desc limit 1" % (
                                         self.house_contract_id, step))[0]
        return step_status

    def landlord(self):
        return HouseContractLandlordInfo(self.house_contract_id)


class HouseContractLandlordInfo(object):
    """业主信息"""

    def __init__(self, contract_id):
        sql = "select * from house_contract_landlord where contract_id='%s' and deleted=0" % contract_id
        self.landlord_info = Mysql().query(sql)[0]
        self.contract_landlord_id = self.landlord_info['contract_landlord_id']
        self.phone = self.landlord_info['phone']
        self.other_contact = self.landlord_info['other_contact']
        self.card_type = self.landlord_info['card_type']
        self.landlord_name = self.landlord_info['landlord_name']
        self.id_card = self.landlord_info['id_card']
        self.landlord_type = self.landlord_info['landlord_type']
        self.mailing_address = self.landlord_info['mailing_address']
        self.is_leaser = self.landlord_info['is_leaser']
        self.email = self.landlord_info['email']
        self.emergency_name = self.landlord_info['emergency_name']
        self.emergency_phone = self.landlord_info['emergency_phone']


class HouseContractEndInfo(HouseContractInfo):
    def __init__(self, contractIdOrNum):
        super(HouseContractEndInfo, self).__init__(contractIdOrNum)
        sql = "select * from house_contract_end where contract_id='%s' and deleted=0" % self.house_contract_id
        self.house_contract_end_info = Mysql().query(sql, nullThrow=False)[0]
        if not self.house_contract_end_info:
            consoleLog("there is no house_contract_end,contract_id: %s" % self.house_contract_id, 'e')
            return
        self.end_id = self.house_contract_end_info['end_id']
        self.end_date = self.house_contract_end_info['end_date']
        self.end_type = self.house_contract_end_info['end_type']
        self.pay_owner = self.house_contract_end_info['pay_owner']
        self.pay_owner_bank_no = self.house_contract_end_info['pay_owner_bank_no']
        self.pay_owner_bank_location = self.house_contract_end_info['pay_owner_bank_location']
        self.receivable_total = self.house_contract_end_info['receivable_total']
        self.payable_totle = self.house_contract_end_info['payable_totle']
        self.payable_date = self.house_contract_end_info['payable_date']
        self.receivable_date = self.house_contract_end_info['receivable_date']
        self.end_audit_status = self.house_contract_end_info['audit_status']
        self.__end_audit_status = self.house_contract_end_info['audit_status']
        self.pay_object = self.house_contract_end_info['pay_object']
        self.bank = self.house_contract_end_info['bank']

    @property
    def end_audit_status_now(self):
        """终止结算实时审核状态"""
        self.__end_audit_status = Mysql().getOne("select audit_status from house_contract_end where contract_id='%s' "
                                                 "and deleted=0" % self.house_contract_id)[0]
        return self.__end_audit_status


class ApartmentInfo(HouseInfo):
    def __init__(self, apartmentIdOrCode):
        apartmentId = Mysql().getAll(
            "select apartment_id,house_id from apartment where (apartment_id='%s' or apartment_code "
            "like '%s%s') and deleted=0 and is_active='Y'" % (apartmentIdOrCode, apartmentIdOrCode, '%'))
        if 1 != len(apartmentId):
            raise ValueError(
                'apartment_id num is not one but: %s! search for:%s' % (len(apartmentId), apartmentIdOrCode))
        super(ApartmentInfo, self).__init__(apartmentId[0][1])
        sql = "select * from apartment where apartment_id='%s' and deleted=0" % apartmentId[0][0]
        self.apartment_info = sqlbase.query(sql)[0]
        self.apartment_id = self.apartment_info['apartment_id']
        self.room_id = self.apartment_info['room_id']
        self.apartment_code = self.apartment_info['apartment_code']
        self.apartment_type = self.apartment_info['apartment_type']
        self.rent_type = self.apartment_info['rent_type']
        self.rent_status = self.apartment_info['rent_status']
        self.fitment_cost = self.apartment_info['fitment_cost']
        self.apartment_cost = self.apartment_info['apartment_cost']
        self.is_active = self.apartment_info['is_active']
        self.rent_price = self.apartment_info['rent_price']
        self.fitment_type = self.apartment_info['fitment_type']
        self.house_contract_id = self.apartment_info['house_contract_id']
        self.zone_id = self.apartment_info['zone_id']
        self.set_delivery_date = self.apartment_info['set_delivery_date']
        self.total_cost = self.apartment_info['total_cost']

    @property
    def room_no(self):
        """房屋编号"""
        if self.rent_type == 'SHARE':
            sql = "select (select dict_value from sys_dict_item where room_no=dict_e_value and deleted=0 limit 1) room_no " \
                  "from house_room where room_id='%s'" % self.room_id
            return Mysql().getOne(sql)[0]
        else:
            return None

    @property
    def apartment_property_name(self):
        """房屋地址+房屋编号"""
        if self.room_no:
            return '%s%s' % (self.property_name, self.room_no)
        else:
            return self.property_name

    @property
    def apartment_contract(self):
        """房源对应出租合同"""
        if 'RENTED' == self.rent_status:
            contract_id = Mysql().getOne(
                "select a.contract_id from apartment_contract a inner join apartment_contract_relation b on a.contract_id=b.contract_id "
                "inner join apartment c on b.apartment_id=c.apartment_id where c.apartment_id='%s' and a.deleted=0 and a.is_active='Y'"
                % self.apartment_id)[0]
            return ApartmentContractInfo(contract_id)
        else:
            return None


class ApartmentContractInfo(ApartmentInfo):
    def __init__(self, contractIdOrNum):
        contractId = Mysql().getAll("select ac.contract_id,a.apartment_id from apartment_contract ac "
                                    "inner join apartment_contract_relation acr on ac.contract_id=acr.contract_id "
                                    "inner join apartment a on a.apartment_id=acr.apartment_id "
                                    "where (ac.contract_id='%s' or ac.contract_num='%s') and ac.deleted=0 " %
                                    (contractIdOrNum, contractIdOrNum))
        if 1 != len(contractId):
            raise ValueError(
                'contract_id number is not one but: %s! search for:%s' % (len(contractId), contractIdOrNum))
        super(ApartmentContractInfo, self).__init__(contractId[0][1])
        sql = "select * from apartment_contract where contract_id='%s'" % contractId[0][0]
        self.apartment_contract_info = Mysql().query(sql)[0]
        self.apartment_contract_id = self.apartment_contract_info['contract_id']
        threading.Thread(target=check_query_table, args=(self.apartment_contract_id, 'apartment_contract')).start()
        # query_apartment_contract = sqlbase.serach("select * from query_apartment_contract where contract_id='%s'" %
        #                                           self.apartment_contract_id, oneCount=False, nullLog=False)
        # query_apartment_contract = Mysql().getAll("select * from query_apartment_contract where contract_id='%s'" % self.apartment_contract_id)
        # if 1 != len(query_apartment_contract):  # 检查出租合同宽表
        #     consoleLog(
        #         "there is no contract in 'query_apartment_contract',contract_id: %s" % self.apartment_contract_id, 'w')
        self.apartment_contract_num = self.apartment_contract_info['contract_num']
        self.is_active = self.apartment_contract_info['is_active']
        if 'N' == self.is_active:
            consoleLog(u'出租合同非有效状态', 'w')
        self.contract_type = self.apartment_contract_info['contract_type']
        self.sign_date = self.apartment_contract_info['sign_date']
        self.sign_body = self.apartment_contract_info['sign_body']
        self.sign_did = self.apartment_contract_info['sign_did']
        self.sign_uid = self.apartment_contract_info['sign_uid']
        self.check_in_date = self.apartment_contract_info['check_in_date']
        self.payment_date = self.apartment_contract_info['payment_date']
        self.rent_start_date = self.apartment_contract_info['rent_start_date']
        self.rent_end_date = self.apartment_contract_info['rent_end_date']
        self.deposit = self.apartment_contract_info['deposit']
        self.audit_status = self.apartment_contract_info['audit_status']
        self.__audit_status = self.apartment_contract_info['audit_status']
        self.delay_date = self.apartment_contract_info['delay_date']
        self.manage_server_fee = self.apartment_contract_info['manage_server_fee']
        self.rental_price = self.apartment_contract_info['rental_price']
        self.sign_id_type = self.apartment_contract_info['sign_id_type']
        self.sign_phone = self.apartment_contract_info['sign_phone']
        self.sign_name = self.apartment_contract_info['sign_name']
        self.sign_sex = self.apartment_contract_info['sign_sex']
        self.sign_is_customer = self.apartment_contract_info['sign_is_customer']
        self.person_id = self.apartment_contract_info['person_id']
        self.contract_status = self.apartment_contract_info['contract_status']
        self.postal_address = self.apartment_contract_info['postal_address']
        self.real_due_date = self.apartment_contract_info['real_due_date']
        self.month_server_fee = self.apartment_contract_info['month_server_fee']
        self.deposit_type = self.apartment_contract_info['deposit_type']
        self.payment_cycle = self.apartment_contract_info['payment_cycle']
        self.entrust_type = self.apartment_contract_info['entrust_type']

    @property
    def audit_status_now(self):
        """出租实时审核状态"""
        self.__audit_status = Mysql().getOne("select audit_status from apartment_contract where contract_id='%s'" %
                                             self.apartment_contract_id)[0]
        return self.__audit_status

    @staticmethod
    def contract_field(contractNumOrId, field):
        """查询合同字段"""
        fieldRetrun = Mysql().getOne(
            "select %s from apartment_contract where (contract_num='%s' or contract_id='%s') and deleted=0" %
            (field, contractNumOrId, contractNumOrId))
        if fieldRetrun:
            return fieldRetrun[0]
        else:
            consoleLog(u'合同：%s 对应字段：%s 查询结果为空' % (contractNumOrId, field))

    def receivables(self):
        """出租合同对应所有未删除的应收"""
        sql = "select * from apartment_contract_receivable where contract_id='%s' and deleted=0" % self.apartment_contract_id
        receivables = Mysql().query(sql)
        receivablesVo = []
        for receivable in receivables:
            receivableVo = Receivable(receivable['receivable_id'])
            receivablesVo.append(receivableVo)
        return receivablesVo

    def custmoer_person(self):
        """承租人信息"""
        sql = "select (select person_id from customer_person_relation cpr where cpr.contract_id=ac.contract_id ) person_id from apartment_contract ac " \
              "where contract_id='%s'" % self.apartment_contract_id
        person_id = Mysql().getOne(sql)[0]
        return CustomerPersonInfo(person_id)


class CustomerPersonInfo(object):
    """承租客户信息"""

    def __init__(self, person_id):
        sql = "select * from customer_person where person_id='%s'" % person_id
        self.customer_info = Mysql().query(sql)[0]
        self.person_id = person_id
        self.customer_num = self.customer_info['customer_num']
        self.address = self.customer_info['address']
        self.gender = self.customer_info['gender']
        self.customer_name = self.customer_info['customer_name']
        self.phone = self.customer_info['phone']
        self.card_type = self.customer_info['card_type']
        self.id_card = self.customer_info['id_card']


class ApartmentContractEndInfo(ApartmentContractInfo):
    """出租合同终止信息"""

    def __init__(self, contract_id):
        super(ApartmentContractEndInfo, self).__init__(contract_id)
        sql = "select * from apartment_contract_end where contract_id='%s' and deleted=0" % contract_id
        self.apartment_contract_end_info = Mysql().query(sql)[0]
        self.end_id = self.apartment_contract_end_info['end_id']
        self.end_contract_num = self.apartment_contract_end_info['end_contract_num']
        self.end_date = self.apartment_contract_end_info['end_date']
        self.end_type = self.apartment_contract_end_info['end_type']
        self.payer_bank_no = self.apartment_contract_end_info['payer_bank_no']
        self.payer_bank_location = self.apartment_contract_end_info['payer_bank_location']
        self.receivable_total = self.apartment_contract_end_info['receivable_total']
        self.receivable_date = self.apartment_contract_end_info['receivable_date']
        self.payable_totle = self.apartment_contract_end_info['payable_totle']
        self.payable_date = self.apartment_contract_end_info['payable_date']
        self.end_reason_type = self.apartment_contract_end_info['end_reason_type']
        self.contract_end_type = self.apartment_contract_end_info['contract_end_type']  # payment_type
        self.bank = self.apartment_contract_end_info['bank']
        self.pay_object = self.apartment_contract_end_info['pay_object']
        self.liquidated_receivable = self.apartment_contract_end_info['liquidated_receivable']
        self.end_type_detail = self.apartment_contract_end_info['end_type_detail']
        self.payer = self.apartment_contract_end_info['payer']
        self.end_audit_status = self.apartment_contract_end_info['audit_status']


class DecorationHouseInfo(object):
    """工程管理房屋信息"""

    def __init__(self, contractNumOrId):
        sql = "select * from %s.decoration_house_info where (contract_num='%s' or contract_id='%s') and deleted=0" % (
            get_conf('db', 'decoration_db'), contractNumOrId, contractNumOrId)
        self.decoration_house_info = Mysql().query(sql, resarch=True)[0]
        self.info_id = self.decoration_house_info['info_id']
        self.house_code = self.decoration_house_info['house_code']
        self.house_id = self.decoration_house_info['house_id']
        self.build_area = self.decoration_house_info['build_area']
        self.entrust_type = self.decoration_house_info['entrust_type']
        self.address = self.decoration_house_info['address']
        self.contract_id = self.decoration_house_info['contract_id']
        self.contract_num = self.decoration_house_info['contract_num']
        self.contract_type = self.decoration_house_info['contract_type']
        self.create_time = self.decoration_house_info['create_time']
        self.create_uid = self.decoration_house_info['create_uid']
        self.entrust_end_date = self.decoration_house_info['entrust_end_date']
        self.entrust_start_date = self.decoration_house_info['entrust_start_date']
        self.housekeep_mange_uid = self.decoration_house_info['housekeep_mange_uid']
        self.city_code = self.decoration_house_info['city_code']
        self.city_name = self.decoration_house_info['city_name']

    @staticmethod
    def searchByInfoId(info_id):
        """根据info_id查询房屋信息
        :param info_id
        :return 房屋信息对象
        """
        sql = "select contract_id from %s.decoration_house_info where info_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), info_id)
        contract_id = Mysql().getOne(sql)[0]
        return DecorationHouseInfo(contract_id)

    def zones(self):
        sql = "select zone_id from %s.funcation_zone where info_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), self.info_id)
        zone_ids = Mysql().getAll(sql)
        zones = []
        if zone_ids:
            for zone_id in zone_ids:
                zones.append(self.Zone(zone_id))
        else:
            consoleLog(u'房屋未分割')
        return zones

    @staticmethod
    class Zone(object):

        def __init__(self, zone_id):
            sql = "select * from %s.funcation_zone where zone_id='%s' and deleted=0" % (
                get_conf('db', 'decoration_db'), zone_id)
            self.zone_id = zone_id
            self.zone_info = Mysql().query(sql[0])
            self.zone_type = self.zone_info['zone_type']
            self.room_no = self.zone_info['room_no']
            self.usearea = self.zone_info['usearea']
            self.zone_orientation = self.zone_info['zone_orientation']
            self.have_toilet = self.zone_info['have_toilet']
            self.toilet_area = self.zone_info['toilet_area']
            self.have_balcony = self.zone_info['have_balcony']
            self.balcony_area = self.zone_info['balcony_area']
            self.window_area = self.zone_info['window_area']
            self.window_type = self.zone_info['window_type']
            self.zone_status = self.zone_info['zone_status']
            self.is_fictitious_room = self.zone_info['is_fictitious_room']


class DecorationProjectInfo(DecorationHouseInfo):
    """工程订单"""

    def __init__(self, contractNumOrId):
        super(DecorationProjectInfo, self).__init__(contractNumOrId)
        sql = "select * from %s.new_decoration_project where info_id='%s' " % (
            get_conf('db', 'decoration_db'), self.info_id)
        self.project_info = Mysql().query(sql, resarch=True)[0]
        self.project_id = self.project_info['project_id']
        self.project_no = self.project_info['project_no']
        self.config_order_no = self.project_info['config_order_no']
        self.one_level_nodes = self.project_info['one_level_nodes']
        self.place_order_date = self.project_info['place_order_date']
        self.config_submit_uid = self.project_info['config_submit_uid']
        self.config_submit_uname = self.project_info['config_submit_uname']
        self.construct_uid = self.project_info['construct_uid']
        self.construct_uname = self.project_info['construct_uname']
        self.closed_water_test_result = self.project_info['closed_water_test_result']
        self.complete_two_nodes = self.project_info['complete_two_nodes']
        self.config_list_status = self.project_info['config_list_status']
        self.config_progress = self.project_info['config_progress']
        self.current_one_node = self.project_info['current_one_node']

    def update(self):
        """更新订单部分字段"""
        sql = "select * from %s.new_decoration_project where info_id='%s' " % (
            get_conf('db', 'decoration_db'), self.info_id)
        newInfo = Mysql().query(sql)[0]
        self.config_order_no = newInfo['config_order_no']
        self.one_level_nodes = newInfo['one_level_nodes']
        self.place_order_date = newInfo['place_order_date']
        self.config_submit_uid = newInfo['config_submit_uid']
        self.config_submit_uname = newInfo['config_submit_uname']
        self.construct_uid = newInfo['construct_uid']
        self.construct_uname = newInfo['construct_uname']
        self.closed_water_test_result = newInfo['closed_water_test_result']
        self.complete_two_nodes = newInfo['complete_two_nodes']
        self.config_list_status = newInfo['config_list_status']
        self.config_progress = newInfo['config_progress']
        self.current_one_node = newInfo['current_one_node']

    @staticmethod
    def searchByInfoId(info_id):
        """根据info_id查询工程订单
        :param info_id
        :return 工程订单对象
        """
        sql = "select contract_id from %s.decoration_house_info where info_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), info_id)
        contract_id = Mysql().getOne(sql)[0]
        return DecorationProjectInfo(contract_id)

    @staticmethod
    def searchByProjectId(project_id):
        """根据project_id查询工程订单
        :param project_id
        :return 工程订单对象
        """
        sql = "select info_id from %s.new_decoration_project where project_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), project_id)
        info_id = Mysql().getOne(sql)[0]
        return DecorationProjectInfo.searchByInfoId(info_id)

    def get_stuff_list(self):
        """获取装修清单配置信息"""
        sql = "select * from %s.new_stuff_list where project_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), self.project_id)
        stuff_lists = Mysql().query(sql)
        return stuff_lists

    def get_config_list(self):
        """获取物品清单配置信息"""
        sql = "select * from %s.new_stuff_list where project_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), self.project_id)
        config_lists = Mysql().query(sql)
        return config_lists

    @property
    def config_suppliers(self):
        """订单所有物品供应商id"""
        sql = "select distinct supplier_id from %s.new_stuff_list where project_id='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), self.project_id)
        supplier_ids = Mysql().getAll(sql)
        if not supplier_ids:
            consoleLog(u'订单配置供应商不存在')
        return supplier_ids


class Receivable(object):
    """出租合同应收"""

    def __init__(self, receivable_id):
        sql = "select * from apartment_contract_receivable where receivable_id='%s' and deleted=0" % receivable_id
        receivable = Mysql().query(sql)[0]
        self.receivable_id = receivable['receivable_id']
        self.contract_id = receivable['contract_id']
        self.finance_num = receivable['finance_num']
        self.money_type = receivable['money_type']
        self.start_date = receivable['start_date']
        self.end_date = receivable['end_date']
        self.receivable_date = receivable['receivable_date']
        self.receivable_money = receivable['receivable_money']
        self.__end_status = receivable['end_status']
        self.end_status = receivable['end_status']
        self.receivable_from = receivable['receivable_from']
        self.end_type = receivable['end_type']

    @property
    def end_status_now(self):
        """实时应收状态"""
        self.__end_status = Mysql().getOne("select end_status from apartment_contract_receivable where receivable_id='%s' "
                                           "and deleted=0" % self.receivable_id)[0]
        return self.__end_status


class Payable(object):
    """委托应付"""

    def __init__(self, payable_id):
        self.payable_id = payable_id
        sql = "select * from house_contract_payable where payable_id='%s' and deleted=0" % self.payable_id
        payable = Mysql().query(sql)[0]
        self.contract_id = payable['contract_id']
        self.finance_num = payable['finance_num']
        self.money_type = payable['money_type']
        self.rent_start_date = payable['rent_start_date']
        self.rent_end_date = payable['rent_end_date']
        self.payable_date = payable['payable_date']
        self.payable_amount = payable['payable_amount']  # 应付总额
        self.end_status = payable['end_status']  # 完结状态
        self.__end_status = payable['end_status']  # 完结状态
        self.end_time = payable['end_time']  # 完结时间
        self.audit_status = payable['audit_status']  # 租金审核状态
        self.__audit_status = payable['audit_status']  # 租金审核状态
        self.end_type = payable['end_type']  # 终止状态
        self.deduction_amount = payable['deduction_amount']  # 扣款金额

    @property
    def end_stuatus_now(self):
        """实时完结状态"""
        self.__end_status = Mysql().getOne("select end_status from house_contract_payable where payable_id='%s' "
                                           "and deleted=0" % self.payable_id)[0]
        return self.__end_status

    @property
    def audit_status_now(self):
        """实时审核状态"""
        self.__audit_status = Mysql().getOne("select audit_status from house_contract_payable where payable_id='%s' "
                                             "and deleted=0" % self.payable_id)[0]
        return self.__audit_status


class RepairOrderInfo(object):
    """报修订单信息"""

    def __init__(self, orderNumOrId):
        sql = "select * from %s.repairs_order where (order_no='%s' or order_id='%s') and deleted=0" % (
            get_conf('db', 'rsm_db'), orderNumOrId, orderNumOrId)
        self.repairs_order_info = Mysql().query(sql)[0]
        self.order_id = self.repairs_order_info['order_id']
        self.order_no = self.repairs_order_info['order_no']
        self.apartment_id = self.repairs_order_info['apartment_id']
        self.apartment_type = self.repairs_order_info['apartment_type']
        self.rent_status = self.repairs_order_info['rent_status']
        self.rent_type = self.repairs_order_info['rent_type']
        self.house_id = self.repairs_order_info['house_id']
        self.room_id = self.repairs_order_info['room_id']
        self.apartment_contract_id = self.repairs_order_info['apartment_contract_id']
        self.apartment_contract_num = self.repairs_order_info['apartment_contract_num']
        self.customer_id = self.repairs_order_info['customer_id']
        self.house_contract_id = self.repairs_order_info['house_contract_id']
        self.house_address = self.repairs_order_info['house_address']
        self.customer_phone = self.repairs_order_info['customer_phone']


def check_query_table(param, type):
    """检查宽表数据是否生成"""
    sql = "select * from query_{} where contract_id='{}'".format(type, param)
    result = Mysql().getOne(sql, research=True, nullLog=False)
    if not result:
        consoleLog('{}宽表：{} 未生成'.format(type, param))
        # else:
        #     consoleLog('宽表数据已生成')

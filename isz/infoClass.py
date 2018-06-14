# -*- coding:utf8 -*-
"""表元素基础信息类"""
from common import sqlbase
from common.base import consoleLog, get_conf

class HouseInfo(object):

    def __init__(self, houseIdOrCode):
        houseId = sqlbase.serach("select house_id from house where (house_id='%s' or house_code like '%s%s') and deleted=0 " % (houseIdOrCode, houseIdOrCode, '%'), oneCount=False)
        if 1 != len(houseId):
            raise ValueError('house_id number is not one but: %s! search for:%s' % (len(houseId), houseIdOrCode))
        sql = "select * from house where house_id='%s' and deleted=0" % houseId[0]
        self.house_info = sqlbase.query(sql)[0]
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
        contractId = sqlbase.serach("select contract_id,house_id from house_contract where (contract_id='%s' or contract_num='%s') and deleted=0" % (contractIdOrNum, contractIdOrNum), oneCount=False, nullLog=False)
        if 1 != len(contractId):
            raise ValueError('contract_id number is not one but: %s! search for:%s' % (len(contractId), contractIdOrNum))
        sql = "select * from house_contract where contract_id='%s' and deleted=0" % contractId[0][0]
        super(HouseContractInfo, self).__init__(contractId[0][1])
        self.house_contract_info = sqlbase.query(sql)[0]
        self.house_contract_id = self.house_contract_info['contract_id']
        query_house_contract = sqlbase.serach("select * from query_house_contract where contract_id='%s'" % self.house_contract_id, oneCount=False)
        if 1 != len(query_house_contract):  # 检查委托合同宽表
            consoleLog("there is no contract in 'query_house_contract',contract_id: %s" % self.house_contract_id, 'w')
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

    # 委托合同实时审核状态
    @property
    def audit_status_now(self):
        self.__audit_status = sqlbase.serach("select audit_status from house_contract where contract_id='%s' and deleted=0" % self.house_contract_id)[0]
        return self.__audit_status

    # 委托合同应付，默认读取未审核的应付租金
    def payables(self, audit_status='NOTAUDIT', money_type='RENT'):
        sql = "select * from house_contract_payable where contract_id='%s' and deleted=0" % self.house_contract_id
        payables = sqlbase.query(sql)
        payablesVo = []
        for payable in payables:
            payableVo = Payable(payable['payable_id'])
            if not audit_status or audit_status == payableVo.audit_status:
                if not money_type or money_type == payableVo.money_type:
                    payablesVo.append(payableVo)
        return payablesVo

    # 委托合同分步审核状态
    def step_status(self, step):
        step_status = sqlbase.serach("select status from house_contract_step_audit_status where contract_id = '%s' and "
                                     "step = '%s' and deleted=0 order by step_id desc limit 1" % (
                                         self.house_contract_id, step))[0]
        return step_status

    # 业主信息
    # def landlord(self):
    #     sql = "select * from house_contract_landlord where contract_id='%s' and deleted=0" % self.house_contract_id
    #     landlord = sqlbase.sera´ch(
    #         "select landlord_name,phone,email,mailing_address,emergency_name,emergency_phone from house_contract_landlord where contract_id='%s' and deleted=0" % self.contract_id)
    #     landlordInfo = sqlbase.query(sql)
    #     return None


class HouseContractEndInfo(HouseContractInfo):

    def __init__(self, contractIdOrNum):
        super(HouseContractEndInfo, self).__init__(contractIdOrNum)
        sql = "select * from house_contract_end where contract_id='%s' and deleted=0" % self.house_contract_id
        self.house_contract_end_info = sqlbase.query(sql, nullThrow=False)[0]
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

    # 终止结算实时审核状态
    @property
    def end_audit_status_now(self):
        self.__end_audit_status = sqlbase.serach("select audit_status from house_contract_end where contract_id='%s' "
                                                 "and deleted=0" % self.house_contract_id)[0]
        return self.__end_audit_status


class ApartmentInfo(HouseInfo):

    def __init__(self, apartmentIdOrCode):
        apartmentId = sqlbase.serach(
            "select apartment_id,house_id from apartment where (apartment_id='%s' or apartment_code "
            "like '%s%s') and deleted=0 and is_active='Y'" % (apartmentIdOrCode, apartmentIdOrCode, '%'),
            oneCount=False)
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


class ApartmentContractInfo(ApartmentInfo):

    def __init__(self, contractIdOrNum):
        contractId = sqlbase.serach("select ac.contract_id,a.apartment_id from apartment_contract ac "
                                    "inner join apartment_contract_relation acr on ac.contract_id=acr.contract_id "
                                    "inner join apartment a on a.apartment_id=acr.apartment_id "
                                    "where (ac.contract_id='%s' or ac.contract_num='%s') and ac.deleted=0 " %
                                    (contractIdOrNum, contractIdOrNum), oneCount=False)
        if 1 != len(contractId):
            raise ValueError(
                'contract_id number is not one but: %s! search for:%s' % (len(contractId), contractIdOrNum))
        super(ApartmentContractInfo, self).__init__(contractId[0][1])
        sql = "select * from apartment_contract where contract_id='%s'" % contractId[0][0]
        self.apartment_contract_info = sqlbase.query(sql)[0]
        self.apartment_contract_id = self.apartment_contract_info['contract_id']
        threading.Thread(target=check_query_table, args=(self.apartment_contract_id, 'apartment_contract')).start()
        query_apartment_contract = sqlbase.serach("select * from query_apartment_contract where contract_id='%s'" %
                                                  self.apartment_contract_id, oneCount=False, nullLog=False)
        if 1 != len(query_apartment_contract):  # 检查出租合同宽表
            consoleLog(
                "there is no contract in 'query_apartment_contract',contract_id: %s" % self.apartment_contract_id, 'w')
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
    def audit_status_now(self):  # 出租实时审核状态
        self.__audit_status = sqlbase.serach("select audit_status from apartment_contract where contract_id='%s'" %
                                             self.apartment_contract_id)[0]
        return self.__audit_status

    @staticmethod  # 查询合同字段
    def contract_field(contractNumOrId, field):
        fieldRetrun = sqlbase.serach(
            "select %s from apartment_contract where (contract_num='%s' or contract_id='%s') and deleted=0" %
            (field, contractNumOrId, contractNumOrId))
        if fieldRetrun:
            return fieldRetrun[0]
        else:
            consoleLog(u'合同：%s 对应字段：%s 查询结果为空' % (contractNumOrId, field))

    # 出租合同对应所有未删除的应收
    def receivables(self):
        sql = "select * from apartment_contract_receivable where contract_id='%s' and deleted=0" % self.apartment_contract_id
        receivables = sqlbase.query(sql)
        receivablesVo = []
        for receivable in receivables:
            receivableVo = Receivable(receivable['receivable_id'])
            receivablesVo.append(receivableVo)
        return receivablesVo


class ApartmentContractEndInfo(ApartmentContractInfo):

    def __init__(self, contract_id):
        super(ApartmentContractEndInfo, self).__init__(contract_id)
        sql = "select * from apartment_contract_end where contract_id='%s' and deleted=0" % contract_id
        self.apartment_contract_end_info = sqlbase.query(sql)[0]
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

    def __init__(self, contractNum):
        sql = "select * from %s.decoration_house_info where contract_num='%s' and deleted=0" % (
            get_conf('db', 'decoration_db'), contractNum)
        self.decoration_house_info = sqlbase.query(sql)[0]
        self.info_id = self.decoration_house_info['info_id']


class DecorationProjectInfo(DecorationHouseInfo):

    def __init__(self, contractNum):
        super().__init__(contractNum)
        sql = "select * from %s.new_decoration_project where info_id='%s' " % (
            get_conf('db', 'decoration_db'), self.info_id)
        self.project_info = sqlbase.query(sql)[0]
        self.project_id = self.project_info['project_id']

    # 获取装修清单配置信息
    def get_stuff_list(self):
        sql = "select * from %s.new_stuff_list where project_id='%s' and deleted=0" % (get_conf('db', 'decoration_db'),
                                                                                       self.project_id)
        stuff_lists = sqlbase.query(sql)
        return stuff_lists

    # 获取物品清单配置信息
    def get_config_list(self):
        sql = "select * from %s.new_stuff_list where project_id='%s' and deleted=0" % (get_conf('db', 'decoration_db'),
                                                                                       self.project_id)
        config_lists = sqlbase.query(sql)
        return config_lists


class Receivable(object):
    """出租合同应收"""

    def __init__(self, receivable_id):
        sql = "select * from apartment_contract_receivable where receivable_id='%s' and deleted=0" % receivable_id
        receivable = sqlbase.query(sql)[0]
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
    def end_status_now(self):  # 实时应收状态
        self.__end_status = \
            sqlbase.serach("select end_status from apartment_contract_receivable where receivable_id='%s' "
                           "and deleted=0" % self.receivable_id)[0]
        return self.__end_status


class Payable(object):
    """委托应付"""

    def __init__(self, payable_id):
        self.payable_id = payable_id
        sql = "select * from house_contract_payable where payable_id='%s' and deleted=0" % self.payable_id
        payable = sqlbase.query(sql)[0]
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
    def end_stuatus_now(self):  # 实时完结状态
        self.__end_status = sqlbase.serach("select end_status from house_contract_payable where payable_id='%s' "
                                           "and deleted=0" % self.payable_id)[0]
        return self.__end_status

    @property
    def audit_status_now(self):
        self.__audit_status = sqlbase.serach("select audit_status from house_contract_payable where payable_id='%s' "
                                             "and deleted=0" % self.payable_id)[0]
        return self.__audit_status

def check_query_table(contract_id, contract_type):  # FF80808163F413680163F42A6D9904CF
    sql = "select * from query_{} where contract_id='{}'".format(contract_type, contract_id)
    result = sqlbase.serach(sql, research=True, nullLog=False)
    if not result:
        consoleLog('宽表合同：{} 未生成'.format(contract_id))

if __name__ == '__main__':
    # end = HouseContractEndInfo('WFL工程1.4-06010149Qx')
    # print(end)
    # check_query_table('FF80808163F413680163F42A6D9904CF', 'apartment_contract')
    ApartmentContractInfo('FF80808163F413680163F42A6D9904CF')

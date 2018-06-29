# -*- coding:utf8 -*-

from collections import OrderedDict
from enum import Enum
from common import sqlbase
from common.base import get_conf
from common.mysql import Mysql

"""字典"""

# 字典参转中
def get_dict_value(dict_e_value, dict_code = None):
    if dict_code:
        dict_code = "and dict_code=%s" % dict_code
    sql = "select dict_value from sys_dict_item where dict_e_value = '%s' and deleted=0 and is_active='Y' %s" % (dict_e_value, dict_code)
    return Mysql().getAll(sql)

class UserInfo(object):

    def __init__(self, phone):
        self.user_info = Mysql().query("select * from sys_user a inner join sys_department b on a.dep_id=b.dep_id "
                                       "where a.user_phone='%s' and a.user_status='INCUMBENCY'" % phone)[0]
        self.user_name = self.user_info['user_name']
        self.user_id = self.user_info['user_id']
        self.user_phone = self.user_info['user_phone']
        self.user_status = self.user_info['user_status']
        self.dep_id = self.user_info['dep_id']
        self.dep_name = self.user_info['dep_name']

# 获取登录用户信息
def getUserInfo():
    exhouseSql = Mysql().getAll("select a.user_name,a.user_id,a.dep_id,b.dep_name from sys_user a inner join sys_department b on a.dep_id=b.dep_id "
                                "where a.user_phone='%s' and a.user_status='INCUMBENCY'" % get_conf('sysUser', 'userphone'))[0]
    userInfo = {
        'user_name': exhouseSql[0],
        'uid': exhouseSql[1],
        'dep_name': exhouseSql[3],
        'did': exhouseSql[2],
    }
    return userInfo
userInfo = getUserInfo()

# 委托合同审核步骤
step_Par = OrderedDict()
step_Par['ONE'] = 'houseContractFrist'
step_Par['TWO'] = 'houseContractSecond'
step_Par['THREE'] = 'houseContractThird'
step_Par['FOUR'] = 'houseContractFour'
step_Par['FIVE'] = 'houseContractFive'
house_contract_dict = {'auditStatus_Par': {'chushen': 'PASS', 'fushen': 'APPROVED'}, 'step_Par': step_Par}

# 付款周期对应免租期天数
free_date_par = {
    'MONTH': 25,
    'SEASON': 30,
    'ONE_YEAR': 50,
    'TOW_MONTH': 30,
    'HALF_YEAR': 40,
    'ALL': 30
}

ROOM_NAME = {
    '01': u'甲',
    'METH': u'甲',
    '02': u'乙',
    'ETH': u'乙',
    '03': u'丙',
    'PROP': u'丙',
    '04': u'丁',
    'BUT': u'丁',
    '05': u'戊',
    'PENT': u'戊',
    '06': u'己',
    'HEX': u'己',
    '07': u'庚 ',
    'HEPT': u'庚 ',
    '08': u'辛',
    'OCT': u'辛',
    '09': u'壬',
    'NON': u'壬',
    '10': u'癸',
    'DEC': u'癸'
}

# 委托合同产权人
landlord = {
    'landlord_name': u'产权人',
    'card_type': 'PASSPORT',
    'id_card': 'huzhao123456',
    'phone': '11111111111',
    'email': 'wangfanglong@ishangzu.com',
    'mailing_address': u'海创基地',
}

class User(Enum):
    """登录用户信息"""

    exhouseSql = Mysql().getAll("select a.user_name,a.user_id,a.dep_id,b.dep_name from sys_user a inner join sys_department b on a.dep_id=b.dep_id "
                                "where a.user_phone='%s' and a.user_status='INCUMBENCY'" % get_conf('sysUser', 'userphone'))[0]
    UID = exhouseSql[1]
    DID = exhouseSql[2]
    NAME = exhouseSql[0]
    D_NAME = exhouseSql[3]

class AuditStatus(Enum):

    APARTMETN_CONTRACT_END_STATUS_REJECT = 'RE_JECT'  # 出租终止驳回
    APARTMETN_CONTRACT_END_STATUS_WAIT_AUDIT = 'NO_AUDIT'  # 出租终止待审核
    APARTMETN_CONTRACT_END_STATUS_AUDITED = 'PASS'  # 出租终止已初审
    APARTMETN_CONTRACT_END_AUDIT_AFTER = 'PASS'  # 出租终止初审关键字
    APARTMETN_CONTRACT_END_APPROVED_AFTER = 'REVIEW'  # 出租终止复审关键字
    HOUSE_CONTRACT_STATUS_WAIT_AUDIT = 'AUDIT'  # 委托待审核
    HOUSE_CONTRACT_STATUS_AUDITED = 'PASS'  # 委托已初审
    HOUSE_CONTRACT_STATUS_APPROVED = 'APPROVED'  # 委托已复审

class AUDIT_STATUS(Enum):

    class APARTMETN_CONTRACT_END(Enum):
        REJECT = 'RE_JECT'
        AUDITED = 'PASS'
        WAIT_AUDIT = 'NO_AUDIT'
        APPROVED = 'RECIEW'

    class HOUSE_CONTRACT(Enum):
        WAIT_AUDIT = 'AUDIT'
        AUDITED = 'PASS'
        APPROVED = 'APPROVED'


# class ApartmentList():
#
#     __fields = ['apartment_id', 'apartment_code']
#     __conditions = {
#         'deleted': 0,
#     }
#
#     @classmethod
#     def set_condition(cls, conditions):
#         if types.DictType == type(conditions):
#             for i in conditions.keys():
#                 cls.__conditions[i] = conditions[i]
#         else:
#             raise ValueError("TypeError:condition is not true type")
#
#     @classmethod
#     def set_retrun(cls, fields):
#         if types.StringType == type(fields):
#             cls.__fields.append(fields)
#         elif types.ListType == type(fields):
#             for field in fields:
#                 cls.__fields.append(field)
#         else:
#             raise ValueError("TypeError:fields is not true type")
#
#     @classmethod
#     def list(cls, oneCount=False):
#         fields = ','.join(cls.__fields)
#         conditions = []
#         for key in cls.__conditions.keys():
#             condition = "%s='%s'" % (key, cls.__conditions[key])
#             conditions.append(condition)
#         conditions = ' and '.join(conditions)
#         sql = "select %s from apartment where deleted=0 and %s" % (fields, conditions)
#         infos = sqlbase.serach(sql, oneCount=oneCount)
#         if infos:
#             if oneCount:
#                 alist = dict(zip(cls.__fields, infos))
#             else:
#                 j = 0
#                 alist = [{}]
#                 for info in infos:
#                     alist[j] = dict(zip(cls.__fields, info))
#             return alist
#         else:
#             raise ValueError('apartment search sql return null')

if __name__ == '__main__':
    # apartment = ApartmentList()
    # apartment.set_retrun('house_id')
    # apartment.set_condition({'apartment_id': '0953b669345811e7801bd89d672b5e48', 'is_active': 'Y'})
    # print apartment.list()

    # apartment = ApartmentInfo('0953b669345811e7801bd89d672b5e48')
    # contract = ApartmentContractInfo('8A2152435DC188BD015DC5DD113458EF')
    # print contract.apartment_contract_info
    # decoration = DecorationProjectInfo('7')
    # print decoration.project_info
    # end = ApartmentContractEndInfo('FF8080816348B9C10163499D4B1D2BCD')
    # print end.apartment_contract_end_info

    # apartment = ApartmentInfo('E48A81416386FE1001638C5A56F000C1')
    # print apartment
    # status = AUDIT_STATUS.APARTMETN_CONTRACT_END.value.REJECT.value
    user = UserInfo('18815286582')
    print user
    # print(status)
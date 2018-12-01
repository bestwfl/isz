# -*- coding:utf8 -*-
import time

from common.base import get_randomString
from common.datetimes import addDays, addMonths, today
from isz.apartment import Apartment
# from common.interface import createApartmentContract
from isz.customer import createCustomer


# @testWithLogin
def test():
    apartmentId = 'HZGS1607300454'
    customer = createCustomer()  # 创建租客，出租合同
    contract_num_sign = u'WFL'  # 合同标识
    contract_num = '%s%s-%s' % (contract_num_sign, time.strftime('%m%d%H%M'), get_randomString(2))
    # contract_num = 'WFL08280959-1r'
    sign_date = addDays(5, addMonths(-11, today()))
    sign_date = today()
    rent_price = 2030
    rent_start_date = addDays(1, sign_date)
    rent_end_date = addDays(-1, addMonths(12, rent_start_date))
    payment_cycle = 'HALF_YEAR'
    sign_phone = '18815286582'
    sign_name = '王方龙'
    sign_id_type = 'IDNO'
    sign_id_no = '330381199203025315'
    # sign_id_no = '111111111111111111'
    contract = Apartment(apartmentId).createApartmentContract(customerInfo=customer,
                                                              rent_price=rent_price, sign_date=sign_date,
                                                              rent_start_date=rent_start_date, rent_end_date=rent_end_date,
                                                              payment_cycle=payment_cycle, contract_num=contract_num,
                                                              sign_phone=sign_phone, sign_id_no=sign_id_no, sign_name=sign_name, sign_id_type=sign_id_type)
    print(contract.apartment_contract_id)
    # 审核合同
    # contract.audit()
    # contract.receiptAndAudit()
    # contract.resign()

if __name__ == '__main__':
    # login()
    test()

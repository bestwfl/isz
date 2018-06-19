# -*- coding:utf8 -*-
import time

from isz.apartment import Apartment
# from common.interface import createApartmentContract
from isz.customer import createCustomer
from common.base import get_randomString
from common.datetimes import addDays, addMonths, today
from common.interface_wfl import testWithLogin

# @testWithLogin
def test():
    apartmentId = 'ZXZ2000910-01'
    customer = createCustomer()  # 创建租客，出租合同
    contract_num_sign = u'APP兼容性'  # 合同标识
    contract_num = '%s-%s%s' % (contract_num_sign, time.strftime('%m%d%H%M'), get_randomString(2))

    sign_date = today()
    rent_price = 2000
    rent_start_date = addDays(1, today())
    rent_end_date = addMonths(12)
    payment_cycle = 'HALF_YEAR'
    sign_phone = '13000000000'
    contract = Apartment(apartmentId).createApartmentContract(customerInfo=customer,
                                                              rent_price=rent_price, sign_date=sign_date,
                                                              rent_start_date=rent_start_date, rent_end_date=rent_end_date,
                                                              payment_cycle=payment_cycle, contract_num=contract_num,sign_phone=sign_phone)
    print contract.apartment_contract_id
    # 审核合同
    # contract.audit()
    # contract.resign()

test()
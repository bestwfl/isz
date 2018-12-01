# -*- coding:utf8 -*-
from common import sqlbase
from common.base import consoleLog
from isz.repair import Repair

if __name__ == '__main__':
    apartments = sqlbase.serach("SELECT apartment_id,apartment_code FROM isz_erp.apartment WHERE is_active='Y' AND deleted=0 "
                                "AND rent_status<>'RENTED' AND rent_type='SHARE' AND city_code='330100' ORDER BY RAND() LIMIT 10",
                                oneCount=False)
    for apartment in apartments:
        consoleLog(u'房源编号：%s ID:%s' % (apartment[1], apartment[0]))
        Repair.createRepair(apartment[0])
        # Repair.cancel('FF808081636379B101636379C2960018')
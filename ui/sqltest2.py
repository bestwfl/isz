# -*- coding:utf8 -*-

import  pymysql
from common.base import consoleLog,get_conf
import time

conn = pymysql.connect(host='192.168.0.200',user='wujun',password='ishangzu@wujun',db='isz_erp', port=33307)
cursor = conn.cursor()
cursor.execute("select ac.contract_id,ac.process_time from (select * from apartment_contract ac,workflow_process wp where ac.contract_id = wp.object_id and ac.deleted = 0 "
               "and wp.object_type = 'APARTMENTCONTRACTE'and wp.process_type = 'APPROVED' ORDER BY wp.process_time ) ac GROUP BY ac.contract_id limit 10")
result=cursor.fetchall()
print result


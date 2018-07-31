# -*- coding:utf8 -*-
import time
from common.interface_wfl import myRequest, consoleLog
from officebase.myexcel import Excel
from common.mysql import Mysql


def housingAuthorityPush():
    """房管局推送"""

    # 房管局数据处理
    # 待处理的数据
    list1 = Excel.getDirExcels('C:\Users\user\Desktop\房管局待处理数据')
    third_object_id = "'" + "','".join(str(i) for i in list1[0]) + "'"
    third_object_id_wu = "'" + "','".join(str(i) for i in list1[1]) + "'"
    consoleLog('委托合同地址不存在房管局申请编号(%s个)：\n %s' % (len(list1[1]), list1[1]))
    # 不是2018-04-23同步的无物业地址的数据
    sql_wu = "select third_object_id from isz_housingauthority_relation where object_status='ADD' and update_time not like '2018-04-23%s' " \
             "and third_object_id in(%s)" % ('%', third_object_id_wu)
    result_wu = Mysql().getAll(sql_wu, nullLog=False)
    if result_wu:
        consoleLog('委托合同物业地址不存在且同步时间非2018-04-23的房管局申请编号：\n %s' %  result_wu)
    else:
        consoleLog('不存在物业地址为空，且同步时间在2018-04-23之后的数据')
    # 预计推送数量
    sql = "SELECT apartment_id FROM apartment WHERE apartment_id IN (SELECT DISTINCT a.apartment_id FROM apartment a INNER JOIN house h " \
          "ON a.house_id = h.house_id INNER JOIN isz_housingauthority_relation c ON c.isz_object_id = h.house_id WHERE a.is_active = 'Y' " \
          "AND a.deleted = 0 AND c.object_status = 'ADD' AND c.third_object_id IN (%s))GROUP BY house_id" % third_object_id
    apartment_id_deal = Mysql().getAll(sql)
    consoleLog('预计需要重新推送的房源id(%s个)：\n %s' % (len(apartment_id_deal), apartment_id_deal))
    # 历史已处理过的，需要去重
    list2 = Excel.getDirExcels('C:\Users\user\Desktop\Work\第三方推送\房管局\房管局问题数据反馈')
    third_object_id2 = "'" + "','".join(str(i) for i in list2[0]) + "'"
    sql2 = "SELECT apartment_id FROM apartment WHERE apartment_id IN (SELECT DISTINCT a.apartment_id FROM apartment a INNER JOIN house h " \
           "ON a.house_id = h.house_id INNER JOIN isz_housingauthority_relation c ON c.isz_object_id = h.house_id WHERE a.is_active = 'Y' " \
           "AND a.deleted = 0 AND c.object_status = 'ADD' AND c.third_object_id IN (%s))GROUP BY house_id" % third_object_id2
    apartment_id_dealed = Mysql().getAll(sql2)
    # 去重处理
    for apartment_id in apartment_id_deal:
        if apartment_id in apartment_id_dealed:
            apartment_id_deal.remove(apartment_id)
    consoleLog('去重后实际需要重新推送的房源id(%s个)：\n %s' % (len(apartment_id_deal), apartment_id_deal))
    apartment_id = apartment_id_deal
    consoleLog('开始房管局数据推送')
    url = 'http://isz.ishangzu.com/isz_thirdparty/openapi/thirdpartyhousepush/housingAuthorityPush.action'
    i = 0
    for a in apartment_id:
        data = {
            "goal": "fornew",
            "object_type": "APARTMENT",
            "object_status": "ADD",
            "objectIds": a
        }
        i = i + 1
        myRequest(url, data, needCookie=False)
        consoleLog(u'%s:APARTMENT_ID:%s  已推送合同资料' % (i, a))
        time.sleep(2)  # 避免高并发对面图片数据丢失
        data = {
            "goal": "fornew",
            "object_type": "APARTMENT",
            "object_status": "APPLE_ISSURE",
            "objectIds": a
        }
        myRequest(url, data, needCookie=False)
        consoleLog(u'%s:APARTMENT_ID:%s  已推送挂牌' % (i, a))
        time.sleep(1)
    consoleLog(u'-------------------房管局数据处理结束--------------------')

if __name__ == '__main__':
    housingAuthorityPush()
    pass

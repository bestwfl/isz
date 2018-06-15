# -*- coding:utf8 -*-

import random
import time
from common import sqlbase
from common.base import consoleLog
from common.interface_wfl import myRequest


def createCustomer():
    """
    新增租前客户
    :return: 返回租客信息字典，给创建承租合同提供使用
    """
    url = 'isz_customer/CustomerController/saveCustomer.action'
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    phone = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
    data = {
        'customer_name': 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S'),  # 姓名
        'phone': phone,  # 手机
        'customer_status': 'EFFECTIVE',  # 状态
        'email': 'isz@ishangzu.com',  # 邮箱
        'wechat': 'wechat',  # 微信
        'constellation': 'VIRGO',  # 星座
        'education': 'BACHELOR',  # 学历
        'belong_did': sqlbase.serach(
            "select dep_id from sys_user where user_phone = '13600000001' and user_status = 'INCUMBENCY'")[0],  # 所属部门
        'belong_uid': sqlbase.serach(
            "select user_id from sys_user where user_phone = '13600000001' and user_status = 'INCUMBENCY'")[0],  # 所属人
        'customer_from': 'FLOOR19',  # 来源
        'rent_class': 'CLASSA',  # 求租等级
        'rent_type': 'GATHERHOUSE',  # 求租类型
        'rent_use': 'RESIDENCE',  # 求租用途
        'rent_fitment': 'FITMENT_SIMPLE',  # 装修情况
        'city_code': '330100',  # 求租城区
        'rent_area_code': '330108',  # 求租地区
        'rent_business_circle_ids': '4',  # 求租商圈
        'office_address': u'海创基地',  # 上班地点
        'address_gd_lng': '120.138631',  # 经度
        'address_gd_lat': '30.186537',  # 纬度
        'rent_rooms': '1',  # 求租户型
        'rent_livings': '1',
        'rent_bathrooms': '1',
        'rent_from_price': '1000.00',  # 求租价格
        'rent_to_price': '2000.00',
        'rent_date': time.strftime('%Y-%m-%d'),  # 希望入住日期
        'rent_people': '2',  # 入住人数
        'area': '28',  # 面积
        'rent_other': 'other demand',  # 其他需求
        'gender': 'MALE',  # 性别
        'marriage': 'UNMARRIED',  # 婚否
        'submit_channels': 'ERP'  # 提交渠道
    }
    if myRequest(url, data):
        customerInfo = sqlbase.serach(
            "select customer_id,customer_name,customer_num from customer where customer_name = '%s'" % data[
                'customer_name'])
        consoleLog(u'租前客户 %s 创建成功' % customerInfo[1])
        return {'customer_id': customerInfo[0], 'customer_name': customerInfo[1], 'customer_num': customerInfo[2]}

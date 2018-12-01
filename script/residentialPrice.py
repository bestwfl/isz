# -*- coding:utf8 -*-

from common.base import consoleLog
from common.interface_wfl import myRequest
from common.mySql import Mysql


def get_residentail_ratio(residential_id, rent_type):
    """获取楼盘房源标准价系数
    :param rent_type: 房源类型
    :param residential_id 楼盘id
    :return [{"apartment_id": 123,"ratio":1.023}]"""
    url = 'http://erp.ishangzu.com/isz_house/ResidentialStandardPriceController/selectModifyPriceApartmentList'
    data = {"residential_id": residential_id, "new_price": "4400", "rent_type": rent_type}
    apartmentList = myRequest(url, data)
    if not apartmentList:
        consoleLog('试算接口异常','e')
        return
    apartmentList = apartmentList.get('obj')
    coefficientResults = []
    for apartment in apartmentList:
        coefficientResult = {'apartment_id': apartment.get('apartment_id')}
        coefficientList = apartment.get('coefficientList')
        ratio = 1
        for coefficient in coefficientList:
            ratio = ratio * coefficient.get('detail').get('ratio_value')
        coefficientResult['ratio'] = '%.3f' % ratio
        coefficientResults.append(coefficientResult)
    return coefficientResults

def get_dict_e_value(value):
    """获取字典项值"""
    sql = "SELECT dict_e_value from sys_dict_item where dict_value='%s' order by create_time desc limit 1" % value
    return Mysql().getOne(sql)[0]

def get_dict_value(evalue):
    """获取字典项中文值"""
    sql = "SELECT dict_value from sys_dict_item where dict_e_value='%s' order by create_time desc limit 1" % evalue
    return Mysql().getOne(sql)[0]

def get_template_ratio(template_type):
    """获取模板系数"""
    ratioTypeSQl = "SELECT a.ratio_type,a.type_id from standard_price_ratio_type a inner	JOIN standard_price_ratio b on a.config_id=b.config_id " \
                   "where b.ratio_status='VALID' and b.template_type='%s'" % template_type
    ratioTypesList = Mysql().query(ratioTypeSQl)
    ratioTypes = {}
    for type in ratioTypesList:
        ratioDetailSQl = "SELECT ratio_key,ratio_key_name,ratio_value,rule from standard_price_ratio_detail where type_id='%s'" % type.get('type_id')
        ratioDetailList = Mysql().query(ratioDetailSQl)
        ratioDetails = {}
        for detail in ratioDetailList:
            if type.get('ratio_type') == 'ORIENTATION':
                ratioDetails[detail.get('ratio_key')] = detail.get('ratio_value')
            elif type.get('ratio_type') in ('USABLE_AREA', 'AREA'):  # 面积
                ratioDetails[detail.get('rule').replace('#x#', 'area').replace('&&', '&')] = detail.get('ratio_value')
            elif type.get('ratio_type') in ('FLOOR_RATIO', 'FLOOR', 'HOUSE_TYPE'):  # 楼层户型
                ratioDetails[detail.get('rule').replace('#x#', 'floor').replace('&&', '&').replace('||', 'or').replace('#y#', 'total_floor')] = detail.get('ratio_value')
            elif type.get('ratio_type') in ('FITMENT',):  # 装修档次
                ratioDetails[detail.get('rule').replace("'#x#'", 'fitment_level').replace('&&', '&')] = detail.get('ratio_value')
            elif type.get('ratio_type') in ('SEASONALITY',):  # 淡旺季
                ratioDetails[detail.get('ratio_key_name')] = detail.get('ratio_value')
            elif type.get('ratio_type') in ('HOUSE_TYPE', 'REMOULD_HOUSE_TYPE'):  # 户型
                ratioDetails[detail.get('rule').replace('#x#', 'rooms')] = detail.get('ratio_value')
            else:
                ratioDetails[get_dict_e_value(detail.get('ratio_key_name'))] = detail.get('ratio_value')
        ratioTypes[type.get('ratio_type')] = ratioDetails
    return ratioTypes

share_template = get_template_ratio('SHARE')
entire_template = get_template_ratio('ENTIRE')

def get_apartment_detail(apartment_id, apartment_type):
    """获取房源属性"""
    if apartment_type == 'SHARE':
        shareSql = "SELECT hr.room_orientation, a.rooms, hr.room_area, h.floor, ( SELECT rbf.floor_name FROM residential_building_floor rbf LEFT JOIN residential_building_unit rbu ON rbu.unit_id = rbf.unit_id WHERE rbu.building_id = rb.building_id ORDER BY rbf.floor_name + 0 DESC LIMIT 1 ) total_floor, a.bathroom_property, a.fitment_level, a.balcony_property FROM apartment a INNER JOIN house h ON a.house_id = h.house_id LEFT JOIN residential r ON r.residential_id = h.residential_id LEFT JOIN residential_building rb ON rb.building_id = h.building_id INNER JOIN house_room hr ON a.room_id = hr.room_id WHERE a.deleted = 0 AND a.apartment_id = '{}'".format(
            apartment_id)
        return Mysql().query(shareSql)
    else:
        entireSql = "SELECT h.orientation, a.rooms, h.build_area, a.side_suite, h.floor, " \
                    "(SELECT rbf.floor_name FROM isz_erp.residential_building_floor rbf " \
                    "LEFT JOIN isz_erp.residential_building_unit rbu ON rbu.unit_id = rbf.unit_id " \
                    "WHERE rbu.building_id = rb.building_id ORDER BY rbf.floor_name + 0 DESC LIMIT 1 ) totle_floors, a.fitment_level " \
                    "FROM isz_erp.apartment a INNER JOIN isz_erp.house h ON a.house_id = h.house_id " \
                    "LEFT JOIN isz_erp.residential r ON r.residential_id = h.residential_id " \
                    "LEFT JOIN isz_erp.residential_building rb ON rb.building_id = h.building_id " \
                    "WHERE a.deleted = 0 AND a.is_active = 'Y' AND a.apartment_id = '{}'".format(apartment_id)
        return Mysql().query(entireSql)

def get_apartment_ratio(apartment_id):
    pass

if __name__ == '__main__':
    print(get_apartment_detail('52625', 'ENTIRE'))

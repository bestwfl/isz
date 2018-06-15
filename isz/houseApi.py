# -*- coding:utf8 -*-

from common import sqlbase
from common.base import get_conf, consoleLog
from common.base import solr
from common.dict import userInfo
from common.interface_wfl import myRequest

# 杭州
# city_code = 330100
# area_code = 310108
# residential_address = u'杭州市 滨江区 浦沿 autoTest'
# business_circle_name = u'浦沿'
# taBusinessCircleString = 4

# 苏州
city_code = 320500
area_code = 215010
residential_address = u'南京市 高新区 枫桥 autoTest'
business_circle_name = u'枫桥'
taBusinessCircleString = 'bad6e2325ee311e69ecfd89d672b5e48'


# 南京
# city_code = 320100
# area_code = 320104
# residential_address = u'南京市 秦淮区 秦虹 autoTest'
# business_circle_name = u'秦虹'
# taBusinessCircleString = '4028808A5500064D01550006584B0028'

# #上海
# city_code = 310100
# area_code = 310115
# residential_address = u'上海市 浦东新区 南码头 autoTest'
# business_circle_name = u'南码头'
# taBusinessCircleString = '4028808A54FFAB5F0154FFAB7B390082'

# 新增楼盘
def creatResidential(cityCode=None, residentialName=None):
    url = 'isz_house/ResidentialController/saveResidential.action'
    residentialName = residentialName if residentialName else u"XX苏州测试楼盘"  # + '-' + time.strftime('%m%d-%H%M%S')
    sql = "SELECT sd.parent_id FROM sys_department sd INNER JOIN sys_user sur ON sur.dep_id = sd.dep_id INNER JOIN sys_position spt ON spt.position_id = sur.position_id " \
          "WHERE sd.dep_district = 320500 AND sd.is_active='Y' AND sd.dep_id <> '00000000000000000000000000000000' AND (spt.position_name LIKE '资产管家%' OR spt.position_name LIKE '综合管家%') AND sd.dep_name NOT LIKE '%培训%'" \
          "ORDER BY RAND() LIMIT 1"
    dutyDepID = sqlbase.serach(sql)[0]
    data = {
        "residential_name": residentialName,
        "residential_jianpin": "auto",
        "city_code": city_code if not cityCode else cityCode,
        "area_code": area_code,
        "taBusinessCircleString": taBusinessCircleString,
        "address": "autoTest",
        "gd_lng": "120.138631",
        "gd_lat": "30.186537",
        "property_type": "ordinary",
        "taDepartString": dutyDepID,
        "byname": "auto"
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT residential_id from residential where residential_name = '%s' and deleted=0" % residentialName.encode(
            'utf-8')
        residentialID = sqlbase.serach(sql)[0]
        residential = {'residentialName': residentialName, 'residentialID': residentialID, 'dutyDepID': dutyDepID}
        consoleLog(u'楼盘‘%s’创建成功' % residentialName)
        return residential


# 新增栋座
def creatBuilding():
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingNew.action'
    residential = creatResidential()
    buildingName = u'1幢'
    data = {
        "property_name": residential['residentialName'],
        "building_name": buildingName,
        "no_building": u"无",
        "housing_type": "ordinary",
        "residential_id": residential['residentialID'],
        "have_elevator": "Y"
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT building_id from residential_building where residential_id = '%s'" % residential['residentialID']
        buildingID = sqlbase.serach(sql)[0]
        residential['buildingID'] = buildingID
        residential['buildingName'] = buildingName
        consoleLog(u'栋座‘%s’创建成功' % buildingName)
        return residential


# 新增单元
def creatUnit():
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingUnit.action'
    residential = creatBuilding()
    # 楼盘下栋座新增单元
    # residentialInfo = sqlbase.serach("select r.residential_name,r.residential_id,rb.building_name,rb.building_id,rd.did from residential r inner join residential_building rb "
    #                                  "on r.residential_id=rb.residential_id inner join residential_department rd on r.residential_id=rd.residential_id "
    #                                  "where r.residential_id='FF80808162FB87C80162FBE191260006'and building_id='FF80808162FB12D10162FBE1929A014F'")
    # residential = {
    #     'residentialName': residentialInfo[0],
    #     'residentialID': residentialInfo[1],
    #     'buildingName': residentialInfo[2],
    #     'buildingID': residentialInfo[3],
    #     'dutyDepID': residentialInfo[4],
    # }
    unitName = u'2单元'
    data = {
        "property_name": residential['residentialName'] + residential['buildingName'],
        "unit_name": unitName,
        "no_unit": u"无",
        "building_id": residential['buildingID']
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT unit_id from residential_building_unit where building_id = '%s' order by create_time desc limit 1" % \
              residential['buildingID']
        unitID = sqlbase.serach(sql)[0]
        residential['unitID'] = unitID
        residential['unitName'] = unitName
        consoleLog(u'单元‘%s’创建成功' % unitName)
        return residential


# 新增楼层
def creatFloor(count=5):
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingFloor.action'
    unit = creatUnit()
    floors = []
    for i in range(count):
        residential = {}
        for key in unit.keys():
            residential[key] = unit[key]
        floorName = i + 1
        data = {
            "property_name": residential['residentialName'] + residential['buildingName'] + residential['unitName'],
            "floor_name": floorName,
            "unit_id": residential['unitID'],
            "building_id": residential['buildingID']
        }
        result = myRequest(url, data)
        if result:
            sql = "SELECT floor_id from residential_building_floor where building_id = '%s' and unit_id = '%s' order by CONVERT(floor_name,SIGNED)" % (
                residential['buildingID'], residential['unitID'])
            floorID = sqlbase.serach(sql, oneCount=False)[i]
            residential['floorID'] = floorID
            residential['floorName'] = floorName
            floors.append(residential)
    consoleLog(u'楼层全部创建成功')
    return floors


# 新增房屋
def creatHouseNum(count=4):
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingHouseNo.action'
    floors = creatFloor()
    houses = []
    for floor in floors:
        for i in range(count):
            residential = {}
            for key in floor.keys():
                residential[key] = floor[key]
            houseNumName = '%s0%s' % (residential['floorName'], i + 1)
            data = {
                "property_name": residential['residentialName'] + residential['buildingName'] + residential[
                    'unitName'] + str(residential['floorName']) + u'层',
                "rooms": "3", "livings": "1", "bathrooms": "2", "kitchens": "1", "balconys": "2",
                "build_area": "120.00", "orientation": "NORTH",
                "house_no": houseNumName,
                "unit_id": residential['unitID'],
                "building_id": residential['buildingID'],
                "floor_id": residential['floorID']
            }
            result = myRequest(url, data)
            if result:
                sql = "SELECT house_no_id from residential_building_house_no where building_id = '%s' and unit_id = '%s' and floor_id = '%s' order by CONVERT(house_no,SIGNED)" % \
                      (residential['buildingID'], residential['unitID'], residential['floorID'])
                houseNumID = sqlbase.serach(sql, oneCount=False)[i]
                residential['houseNumID'] = houseNumID
                residential['houseNumName'] = houseNumName
                houses.append(residential)
    consoleLog(u'房号全部新增成功')
    return houses


# 新增自营房源
def addHouse():
    url = 'isz_house/HouseController/saveHouseDevelop.action'
    houses = creatHouseNum()
    houseIds = []
    for house in houses:
        residential = {}
        for key in house.keys():
            residential[key] = house[key]
        # personInfo = sqlbase.serach("select user_id,dep_id from sys_user where user_phone = '18815286582'")
        personInfo = userInfo
        data = {
            "residential_name_search": residential['residentialID'],
            "building_name_search": residential['buildingID'],
            "unit_search": residential['unitID'],
            "house_no_search": residential['houseNumID'],
            "residential_name": residential['residentialName'],
            "building_name": residential['buildingName'],
            "unit": residential['unitName'],
            "floor": residential['floorName'],
            "house_no": residential['houseNumName'],
            "residential_address": residential_address,
            "city_code": city_code,
            "area_code": area_code,
            "business_circle_id": "4",
            "contact": "test",
            "did": personInfo['did'],
            "uid": personInfo['uid'],
            "house_status": "WAITING_RENT",
            "category": "NOLIMIT",
            "source": "INTRODUCE",
            "rental_price": "2500.00",
            "rooms": "3",
            "livings": "1",
            "kitchens": "1",
            "bathrooms": "2",
            "balconys": "2",
            "build_area": "120",
            "orientation": "NORTH",
            "residential_id": residential['residentialID'],
            "building_id": residential['buildingID'],
            "unit_id": residential['unitID'],
            "floor_id": residential['floorID'],
            "house_no_id": residential['houseNumID'],
            "business_circle_name": business_circle_name,
            "contact_tel": "18815286582"
        }
        result = myRequest(url, data)
        if result:
            sql = "select house_develop_id from house_develop where house_no_id = '%s'" % residential['houseNumID']
            houseDevelogID = sqlbase.serach(sql)[0]
            residential['houseDevelogID'] = houseDevelogID
            houseIds.append(residential)
    consoleLog(u'审核房源全部新增成功')
    return houseIds


# 审核自营房源
def auditHouse():
    url = 'isz_house/HouseController/auditHouseDevelop.action'
    houseIds = addHouse()
    houseInfos = []
    for houseId in houseIds:
        houseInfo = {}
        for key in houseId.keys():
            houseInfo[key] = houseId[key]
        data = {
            "residential_name_search": houseInfo['residentialID'],
            "building_name_search": houseInfo['buildingID'],
            "unit_search": houseInfo['unitID'],
            "house_no_search": houseInfo['houseNumID'],
            "residential_name": houseInfo['residentialName'],
            "building_name": houseInfo['buildingName'],
            "floor": houseInfo['floorName'],
            "house_no_suffix": "xxx",
            "residential_address": residential_address,
            "residential_department_did": houseInfo['dutyDepID'],
            "house_status": "WAITING_RENT",
            "category": "NOLIMIT",
            "rental_price": "2500.00",
            "build_area": "120.00",
            "rooms": "3",
            "livings": "1",
            "kitchens": "1",
            "bathrooms": "2",
            "balconys": "2",
            "orientation": "NORTH",
            "source": "INTRODUCE",
            "houseRent": {
                "house_status": "WAITING_RENT",
                "category": "NOLIMIT",
                "source": "INTRODUCE",
                "rental_price": "2500.00"
            }, "audit_status": "PASS",
            "building_id": houseInfo['buildingID'],
            "residential_id": houseInfo['residentialID'],
            "unit_id": houseInfo['unitID'],
            "unit": houseInfo['unitName'],
            "floor_id": houseInfo['floorID'],
            "house_no_id": houseInfo['houseNumID'],
            "house_no": houseInfo['houseNumName'],
            "area_code": area_code,
            "city_code": city_code,
            "house_develop_id": houseInfo['houseDevelogID'],
            "update_time": sqlbase.serach(
                "SELECT update_time from house_develop where house_develop_id = '%s'" % houseInfo['houseDevelogID'])[0],
            # "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "audit_content": u"同意"
        }
        result = myRequest(url, data)
        if result:
            sql = "select house_id,house_code from house where residential_id = '%s' and house_no_id = '%s'" % (
                houseInfo['residentialID'], houseInfo['houseNumID'])
            house = sqlbase.serach(sql)
            houseInfo['houseID'] = house[0]
            houseInfo['houseCode'] = house[1]
            # 避免等待时间太长，生成的房源没有出来，此处调用solr的增量操作
            # solr('house', get_conf('testCondition', 'test'))
            consoleLog('%s ADD SUCCESSFUL!' % data['house_no'])
            houseInfos.append(houseInfo)
    consoleLog(u'开发自营房源全部生成成功')
    return houseInfos


if __name__ == '__main__':
    auditHouse()

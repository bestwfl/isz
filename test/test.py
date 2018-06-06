# -*- coding:utf8 -*-
import random

from isz.apartment import Apartment
from isz.finance import Finance
from isz.houseContract import HouseContract
from common import sqlbase
from common.base import consoleLog
from common.interface import receipt
from common.interface_wfl import testWithLogin

# @testWithLogin
def test():
    # user = '13600000000'
    # password = '2'
    # sql = "select b.property_name,d.certificate_type,a.certificate_type_id,a.common_case,a.contract_type,c.card_type,c.contract_landlord_id,c.create_uid,c.create_time,c.deleted," \
    #       "c.email,c.emergency_name,c.emergency_phone,c.id_card,c.is_common_rent,c.is_leaser,c.landlord_name,c.landlord_type,c.mailing_address,c.phone,c.property_card_id,c.property_owner_type," \
    #       "c.update_time,c.update_uid,b.house_code,b.build_area,a.is_new_data,e.is_approved_need,e.is_audit_need,e.is_save_need,a.production_address,a.property_use,a.entrust_type,a.house_id,a.pledge" \
    #       " from house_contract a inner join house b on a.house_id=b.house_id inner join house_contract_landlord c on c.contract_id=a.contract_id inner join contract_certificate_type d on " \
    #       "a.certificate_type_id=d.certificate_type_id inner join house_contract_file_type_detail e on a.contract_id=e.contract_id and e.deleted=0 where a.contract_id='%s'" % contract_id
    # contractInfoSql = sqlbase.serach(sql)
    # idCardInfo = "select a.attachment_id,a.img_id,a.sort,CONCAT('http://image.ishangzu.com/',b.src) from house_contract_attachment a inner join image b on a.img_id=b.img_id " \
    #              "where a.contract_id='%s' and a.deleted=0 and a.attachment_type='%s'" % (contract_id, contractInfoSql[5])

    # contractInfo = {
    #     'address': contractInfoSql[0],
    #     'certificate_type': contractInfoSql[1],
    #     'certificate_type_id': contractInfoSql[2],
    #     'common_case': contractInfoSql[3],
    #     'contract_type': contractInfoSql[4],
    #     #'landlordInfo':
    #         'card_type': contractInfoSql[5],
    #         'contract_landlord_id': contractInfoSql[6],
    #         'create_time': contractInfoSql[7],
    #         'create_uid': contractInfoSql[8],
    #         'deleted': contractInfoSql[9],
    #         'email': contractInfoSql[10],
    #         'emergency_name': contractInfoSql[11],
    #         'emergency_phone': contractInfoSql[12],
    #         'idCardPhotos': {},
    #         'id_card': contractInfoSql[13],
    #         'is_common_rent': contractInfoSql[14],
    #         'is_leaser': contractInfoSql[15],
    #         'landlord_name': contractInfoSql[16],
    #         'landlord_type': contractInfoSql[17],
    #         'mailing_address': contractInfoSql[18],
    #         'phone': contractInfoSql[19],
    #         'property_card_id': contractInfoSql[20],
    #         'property_owner_type': contractInfoSql[21],
    #         'update_time': contractInfoSql[22],
    #         'update_uid': contractInfoSql[23],
    #     'house_code': contractInfoSql[24],
    #     'inside_space': contractInfoSql[25],
    #     'is_new_data': contractInfoSql[26],
    #    # 'productionVos':
    #         'is_approved_need': contractInfoSql[27],
    #         'is_audit_need': contractInfoSql[28],
    #         'is_save_need': contractInfoSql[29],
    #     'production_address': contractInfoSql[30],
    #     'property_use': contractInfoSql[31],
    #     'entrust_type': contractInfoSql[32],
    #     'house_id': contractInfoSql[33],
    #     'pledge':contractInfoSql[34]
    # }
    # certificateType = sqlbase.serach("select certificate_type from contract_certificate_type where certificate_type_id='%s' and deleted=0" % contractInfo['certificate_type_id'])
    # login(user, password)
    # houseSql = "select a.house_id,a.residential_id,a.building_id,a.house_code,a.build_area,a.property_name,a.city_code,a.area_code from house a where a.deleted=0 and a.city_code like '330%' " \
    #            "AND a.property_name like 'WFL%' and not EXISTS(select * from house_contract b where b.house_id=a.house_id ) order by rand() limit 1"
    # houseSql = "select * from house_contract where contract_id='FF80808161796D5601617ED22076014D' limit 1"
    # exhouseSql = sqlbase.serach(houseSql)
    # houseInfo = {'houseID': exhouseSql[0], 'residentialID': exhouseSql[1], 'buildingID': exhouseSql[2],'houseCode': exhouseSql[3],'buildArea': exhouseSql[4],
    #              'propertyName': exhouseSql[5], 'cityCode': exhouseSql[6],'areaCode': exhouseSql[7]}
    # print houseInfo['houseID'], houseInfo['houseCode'], houseInfo['propertyName']
    # myEntrust_type = 'SHARE'
    # myApartment_type = 'BRAND'
    # apartmentId = addHouseContractAndFitment_New(apartment_type=myApartment_type, entrust_type=myEntrust_type,
    #                                          sign_date=today(),owner_sign_date=today(), entrust_start_date=today(),
    #                                          entrust_end_date=addDays(-1, addMonths(13)),delay_date=addDays(-1, addMonths(16)),
    #                                          rent=1234, parking=123, rooms=3,fitmentCost=88888, houseInfo=houseInfo)
    # print "'%s':'%s':'%s'" % (exhouseSql[3], apartmentId, houseInfo['houseID'])

    contract = HouseContract(u'WFL工程BUG-04121602IP')
    contract.audit('fushen')

@testWithLogin
def test2():
    fin = Finance()
    # sql = "select DISTINCT a.receivable_id from apartment_contract_receivable a inner join apartment_contract b on a.contract_id=b.contract_id and b.deleted=0 and b.contract_status<>'CANCEL' inner join apartment_contract_receipts c on c.receivable_id=a.receivable_id and c.receipts_date <= CONCAT('2015-12-31', ' 23:59:59') and c.deleted=0 where a.end_status in ('HASGET','PARTGET') and a.deleted=0 and b.contract_num NOT in ('WB1-0070791','ISZWY(CZ)-0000269','ISZWY(CZ)-0001288','ISZWY(CZ)-0001288','WB1-0071977','WB1-0068237','WB1-0069391','WB1-0069391','WB1-0069391','WB1-0073856','WB1-0068392','WB1-0074356','WB1-0068438','WB1-0072831','WB1-0067046','WB1-0061284','WB1-0068236','ISZWY(CZ)-0000683','WB1-0069433','WB1-0068429','WB1-0064325','WB1-0062904','WJ1-0001114','新科C-H0000986')"
    sql = "select DISTINCT a.receivable_id from apartment_contract_receivable a inner join apartment_contract b on a.contract_id=b.contract_id and b.deleted=0 and b.contract_status<>'CANCEL' inner join apartment_contract_receipts c on c.receivable_id=a.receivable_id and c.receipts_type='INTRANSFER' and c.deleted=0 where a.end_status in ('HASGET') and a.deleted=0;"
    receivables = sqlbase.serach(sql, oneCount=False)
    print len(receivables)
    for receivable_id in receivables:
        fin.endReceivable(receivable_id)

@testWithLogin
def test3():
    receipt('apartmentContract', 'FF80808162BDD3690162BE0656D4003A')

def test4():
    apartment = Apartment('FF80808162B9204D0162CC40E26B0B5E')
    detail = apartment.selectShareHouseDetail()
    # detail = apartment.selectShareHouseDetail()['obj']['houseImgList']
    # detail = apartment.selectShareHouseDetail()['obj']['houseRoomImgList']
    # detail = apartment.selectShareHouseDetail()['obj']['onlineHouseInfo']['agent_description'] #管家说
    # detail = apartment.selectShareHouseDetail()['obj']['onlineHouseInfo']['door_model_describing'] #房源描述
    # detail = apartment.selectShareHouseDetail()['obj']['onlineHouseInfo']['position_description'] #周边描述
    print detail

list = [( None,736,'丁','顶/墙/地面处理','','地面找平','M2',42,5.9,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,247.80,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','顶/墙/地面处理','','加气砖砌墙及粉刷','㎡',140,7.05,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,987.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','顶/墙/地面处理','','原墙面铲灰','㎡',3,4.9,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,14.70,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','顶/墙/地面处理','','墙顶面乳胶漆（原白墙/顶）','㎡',15,24,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,360.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','顶/墙/地面处理','','批腻子','㎡',15,24,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,360.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','顶/墙/地面处理','','色块数量','块',150,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,150.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','顶/墙/地面处理','','房间标语喷','间',88,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,88.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','水电工程','','电路改造 暗装','延米  ',43,7.5,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,322.50,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','进场主材','','新增开关、插座（含弱电箱插座）','个',15,4,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,60.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','进场主材','','晾衣杆','根',82,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,82.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','杂项','','打空调孔','个',80,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,80.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','成品安装','','房间灯具','个',58,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,58.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','成品安装','','木地板','M2',70,5.9,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,413.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'丁','成品安装','','踢脚线（木质)','M',13,10.4,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,135.20,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','拆除、新做入户防盗门','套',1000,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,1000.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','活动家具拆除','项',50,12,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,600.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','门/窗户拆除','项  ',80,8,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,640.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','柜类拆除（房间固定衣柜等）','㎡',66.22,38,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,2516.36,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','地板拆除及垃圾清运','㎡',13,1.7,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,22.10,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','吊顶拆除及垃圾清运','㎡',20,15.2,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,304.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','墙地砖拆除及垃圾清运','㎡',28,22.5,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,630.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','拆除','','拆墙裙','平方米',20,6,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,120.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','地面找平','M2',42,1.8,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,75.60,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','加门垛、包原门洞','项',120,3,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,360.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','原墙面铲灰','㎡',3,74.8,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,224.40,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','墙顶面乳胶漆（原白墙/顶）','㎡',15,74.8,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,1122.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','批腻子','㎡',15,74.8,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,1122.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','街道（含厨房）个性化喷绘','项',278,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,278.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','顶/墙/地面处理','','顶面包水管','米',150,0.9,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,135.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','水电工程','','电路改造 暗装','延米  ',43,22,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,946.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','水电工程','','水路改造 明装','M',42,6.9,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,289.80,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','综合服务','','保洁','M2',8,89.14,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,713.12,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','进场主材','','路由器支架、路由器','套',144,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,144.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','进场主材','','新增开关、插座（含弱电箱插座）','个',15,6,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,90.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','进场主材','','新增强电箱及配套（含空开和漏保）','套',298,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,298.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','杂项','','消防套装','套',90,4,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,360.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','杂项','','材料搬运费（含二次搬运费）','间',100,4,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,400.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','杂项','','无电梯房源，二次搬运费补贴','层',100,5,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,500.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','杂项','','垃圾外运费（间、车按实际情况确定）','车',600,2,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,1200.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','杂项','','其他费用','项',1,768,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,768.00,'DRAFT','原业主遗留铝合金窗户维修80，乙房间窗户护栏160，丁房间包立管228，阳台原业主遗留主下水管更换及阳台窗户上封口300','','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','杂项','','老房全装项目补贴（50平方米以上）','项',500,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,500.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','成品安装','','木地板','M2',70,0,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,0.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','成品安装','','踢脚线（木质)','M',13,0,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,0.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','成品安装','','楼梯不锈钢栏杆','M',160,1.46,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,233.60,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','成品安装','','铝合金门窗','㎡',300,3.83,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,1149.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' ) , ( None,736,'公区','成品安装','','亚克力卡槽','个',40,1,'8AB398CA5CF3F759015D0C4456210023','杭州兴庭装饰有限公司','1970-01-02 00:00:00','1970-01-02 00:00:00',0,40.00,'DRAFT',None,'','',None,None,'','1970-01-02 00:00:00',None,0,'2018-06-02 12:30:28','1614','2018-06-02 12:30:28','1614' )]

class Test():

    def test2(self):
        print  123

    @staticmethod
    def test1():
        print 123


if __name__ == '__main__':
    # paybles = HouseContract(u'WFL工程1.4-06010149Qx').payables()
    Test().test2()


# -*- coding:utf8 -*-
import os
import time
from common.base import consoleLog, get_randomString
from common.mysql import Mysql
from officebase.myexcel import Excel
import xlwt
from xlutils.copy import copy

# path = 'C:\Users\user\Desktop\嗨住楼盘汇总.xlsx'.decode('utf-8')
# dirlist = os.listdir(path)
# list_with_address = []
# list_without_address = []
# for filename in dirlist:
#     filepath = path + "\\" + filename
#     excel = Excel(filepath)
#     i = 3
#     cell_house = excel.readCell(i, 2)
#     while cell_house:
#         cell_house = excel.readCell(i, 2)
#         cell_address = excel.readCell(i, 3)
#         if cell_house:
#             if not str == type(cell_house):
#                 cell_house = str(cell_house).replace("\n", "").replace(".0", "")
#             if u'无' in cell_address:
#                 list_without_address.append(cell_house)
#             else:
#                 list_with_address.append(cell_house)
#         i = i + 1
# print "list_with_address:\n     %s" % list_with_address
# print "list_without_address:\n     %s" % list_without_address

filepath = 'C:\Users\user\Desktop\嗨住楼盘数据\嗨住楼盘汇总.xlsx'.decode('utf-8')
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1')
if os.path.exists(filepath):
    consoleLog('开始读取嗨住楼盘数据')
    i = 1
    excel = Excel(filepath)
    hizhu_name = excel.readCell(i, 4)
    hizhu_res = {}
    while hizhu_name:
        hizhu_name = excel.readCell(i, 4)
        hizhu_citycode = excel.readCell(i, 3)
        hizhu_id = excel.readCell(i, 1)
        hizhu_scope = excel.readCell(i, 8)
        hizhu_region_name = excel.readCell(i, 5)
        hizhu_scope_name = excel.readCell(i, 6)
        hizhu_estate_address = excel.readCell(i, 9)
        city_code = None
        if hizhu_name:
            if hizhu_citycode == '001009001':
                city_code = '310100'
            elif hizhu_citycode == '001010001':
                city_code = '320100'
            elif hizhu_citycode == '001010013':
                city_code = '320500'
            else:
                consoleLog('第 %s 城市识别异常' % i)
            hizhu_re = {
                'hizhu_name': hizhu_name,
                'hizhu_citycode': city_code,
                'hizhu_id': hizhu_id,
                'hizhu_scope': hizhu_scope,
                'hizhu_region_name': hizhu_region_name,
                'hizhu_scope_name': hizhu_scope_name,
                'hizhu_estate_address': hizhu_estate_address,
            }
            hizhu_res[i] = hizhu_re
        i = i + 1
    consoleLog('开始查询ISZ数据')
    sql = "SELECT t.residential_id,t.city_code,t.residential_name,(select name from sys_district where code=t.city_code) city_name FROM residential t " \
          "LEFT JOIN sys_district disArea ON t.area_code = disArea. CODE " \
          "LEFT JOIN sys_district disCity ON t.city_code = disCity. CODE " \
          "WHERE t.deleted = 0 AND t.is_show = '1' and t.city_code in (310100,320100,320500) "
    # sql = "select t.residential_id,t.city_code,t.residential_name,(select name from sys_district where code=t.city_code) city_name from residential t " \
    #       "where t.residential_id in (SELECT a.residential_id from apartment a where a.online_status='ONLINE' " \
    #       "and a.is_active='Y' and a.deleted=0) and t.deleted = 0 AND t.is_show = '1' and t.city_code in (310100,320100,320500)"
    isz_residentials = Mysql().getAll(sql)
    j = 1
    sheet.write(0, 0, u'嗨住小区ID')
    sheet.write(0, 1, u'嗨住小区名称')
    sheet.write(0, 2, u'嗨住商圈ID(scope)')
    sheet.write(0, 3, u'嗨住小区地址s')
    sheet.write(0, 4, u'嗨住小区城区')
    sheet.write(0, 5, u'嗨住小区商圈')
    sheet.write(0, 6, u'爱上租小区名称')
    sheet.write(0, 7, u'爱上租小区ID')
    sheet.write(0, 8, u'城市')
    consoleLog('开始写入EXCEL')
    for residential in isz_residentials:
            sheet.write(j, 6, residential[2].decode('utf-8'))
            sheet.write(j, 7, residential[0].decode('utf-8'))
            sheet.write(j, 8, residential[3].decode('utf-8'))
            for hizhu in hizhu_res.values():
                if residential[2].decode('utf-8') == hizhu['hizhu_name']:
                    if residential[1] == hizhu['hizhu_citycode']:
                        sheet.write(j, 0, hizhu['hizhu_id'])
                        sheet.write(j, 1, hizhu['hizhu_name'])
                        sheet.write(j, 2, hizhu['hizhu_scope'])
                        sheet.write(j, 3, hizhu['hizhu_estate_address'])
                        sheet.write(j, 4, hizhu['hizhu_region_name'])
                        sheet.write(j, 5, hizhu['hizhu_scope_name'])
            consoleLog('第 %s 条写入成功' % j)
            j = j + 1

fileName = 'test-newExcel-%s.xls' % time.strftime('%m%d-%H%M%S')
newfilepath = ("C:\Users\user\Desktop\嗨住楼盘数据\\%s" % fileName).decode('utf-8')
wbk.save(newfilepath)


# newBook = copy(excel.book)
# newSheet = newBook.get_sheet(0)
# newSheet.write(i-1, 13, str('123'))
# newBook.save("C:\Users\user\Desktop\\test.xls")

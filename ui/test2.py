# -*- coding:utf8 -*-
from common import sqlbase


#
# list = []
# resid = {'abc': 123}
# for i in range(10):
#     resid2 = {'abc': resid['abc']}
#     resid2['index'] = i
#     list.append(resid2)
# print list


resid = {'residentialID': u'FF80808160FD0864016101BBE62704BB',
 'buildingName': u'1\u5e62',
 'unitName': u'1\u5355\u5143',
 'unitID': u'FF80808160FD0864016101BBE74204BF',
 'residentialName': u'WFL\u6d4b\u8bd5\u4e13\u7528\u676d\u5dde\u697c\u76d8',
 'dutyDepID': u'10083',
 'buildingID': u'FF80808160FD0864016101BBE6F604BE'}
abc = {}
for key in resid.keys():
    print key
    abc[key] = resid[key]
print abc
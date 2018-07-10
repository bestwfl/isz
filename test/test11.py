# -*- coding:utf8 -*-
from common.interface_wfl import upLoadPhoto

# IMG_LAYOUT = upLoadPhoto(url='http://decorate.ishangzu.com/isz_decoration/DecorationFileController/uploadPhoto', filename='LAYOUT.png', filepath=r"C:\Users\user\Desktop\Image\\")
# data = {
#     "curOneLevelNode": None,
#     "curTwoLevelNode": None,
#     "deliver_room_date": None,
#     "house_attachs": [{
#         "attach_type": "PUBLIC_TOILET_1",
#         "imgs": [{
#             "url": None,  # IMG_PUBLIC_TOILET_1.url,
#             "img_id": None,  # IMG_PUBLIC_TOILET_1.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 0,
#             "type": "PUBLIC_TOILET_1"
#         }]
#     }, {
#         "attach_type": "KITCHEN_1",
#         "imgs": [{
#             "url": None,  # IMG_KITCHEN_1.url,
#             "img_id": None,  # IMG_KITCHEN_1.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 1,
#             "type": "KITCHEN_1"
#         }]
#     }, {
#         "attach_type": "PARLOUR_1",
#         "imgs": [{
#             "url": None,  # IMG_PARLOUR_1.url,
#             "img_id": None,  # IMG_PARLOUR_1.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 2,
#             "type": "PARLOUR_1"
#         }]
#     }, {
#         "attach_type": "METH",
#         "imgs": [{
#             "url": None,  # IMG_METH.url,
#             "img_id": None,  # IMG_METH.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 3,
#             "type": "METH"
#         }]
#     }, {
#         "attach_type": "ETH",
#         "imgs": [{
#             "url": None,  # IMG_ETH.url,
#             "img_id": None,  # IMG_ETH.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 4,
#             "type": "ETH"
#         }]
#     }, {
#         "attach_type": "PROP",
#         "imgs": [{
#             "url": None,  # IMG_PROP.url,
#             "img_id": None,  # IMG_PROP.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 5,
#             "type": "PROP"
#         }]
#     }, {
#         "attach_type": "BALCONY_1",
#         "imgs": [{
#             "url": None,  # IMG_BALCONY_1.url,
#             "img_id": None,  # IMG_BALCONY_1.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 6,
#             "type": "BALCONY_1"
#         }]
#     }, {
#         "attach_type": "BALCONY_2",
#         "imgs": [{
#             "url": None,  # IMG_BALCONY_2.url,
#             "img_id": None,  # IMG_BALCONY_2.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 7,
#             "type": "BALCONY_2"
#         }]
#     }],
#     "layout_attachs": [{
#         "attach_type": "LAYOUT",
#         "imgs": [{
#             "url": IMG_LAYOUT.url,
#             "img_id": IMG_LAYOUT.id,
#             "create_name": "",
#             "create_dept": "",
#             "create_time": "",
#             "sort": 0,
#             "type": ""
#         }]
#     }],
#     "project_id": '123',
#     "remark": None
# }
# for house_attach in data['house_attachs']:
#     IMG = upLoadPhoto(url='http://decorate.ishangzu.com/isz_decoration/DecorationFileController/uploadPhoto', filename='%s.png' % house_attach['attach_type'],
#                       filepath=r"C:\Users\user\Desktop\Image\\")
#     house_attach['imgs'][0]['url'] = IMG.url
#     house_attach['imgs'][0]['id'] = IMG.id
# print data
from common.mysql import Mysql
from isz.contractBase import ContractBase

file = ContractBase.FileType()
print file.getFileId('附记页')
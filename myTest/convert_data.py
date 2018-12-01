# -*- coding:utf8 -*-

# ready_data = "@house_info = select house_id,house_code from house where house_id='100412' and deleted=0;@user_info = {'type':'interface','id':'123','data':{}}"
# ready_data_after = {}
# # print ready_data.split(';')
# i = 0
# for item in ready_data.split(';'):
#     i = i + 1
#     if item.startswith('@'):
#         param_key, param_method = item.split('=', 1)
#         if item.split('=', 1)[1].strip().startswith('select'):
#             item_sql = item.split('=', 1)[1].strip()
#             ready_data_after[item.split('=')[0].strip()] = Mysql().query(item_sql)[0]
#         else:
#             data = eval(item.split('=')[1].strip())
#             ready_data_after[item.split('=')[0].strip()] = data
#     else:
#         consoleLog('第%s个参数识别异常，请规范录入' % i)
# param_name = '@user_info.type'
# param_name_after = param_name.split('.')
# if param_name_after[0] in ready_data_after.keys():
#     try:
#         print(ready_data_after[param_name_after[0]][param_name_after[1]])
#     except KeyError:
#         consoleLog('初始化参数不存在')
data = {
    "house_info": "@house_info",
    "house_code": "@house_info.house_code",
    "house_id": "@house_info.house_id",
    "stardate": "@star_date",
    "user_info": "@user_info",
    "user_info_audit": "@user_info.isReCreate"
}
# str = "select * from house where house_id='@house_id' and house_code='@house_code' and deleted=0"
# print str[1:]
# if isinstance(data, dict):
#     d = OrderedDict(data)
#     for k, v in data.items():
#         print(k, v)
# A = namedtuple('A', 'x y')
# a = A(1, 2)
# print(a)
# list1 = [{"name": "a", "value": "A"}]
# list2 = ["1", 2, 3, 4, 5, 6, 7, 8, 9, 'a']
# for i in list2:
#     if type(i) is int:
#         print str(i.isdigit())
#         print list2.index(i), i
#         i = str(i)
# print list2
# s = 'sdajlsdkajsldk'
# s.split()
# for i in list1.item():
#     print i
# b = eval("'2018-06-11'")
# print b

class MyException(Exception):
    def __int__(self, *args):
        self.args = args


class executeInterfaceException(MyException):
    def __int__(self):
        self.args = ('接口执行异常',)
        self.message = '接口执行异常'


class getResponException(MyException):
    def __int__(self, message=None):
        self.args = ('执行接口去返回值异常',)
        self.message = '执行接口去返回值异常' if not message else message


# -*- coding:utf8 -*-
from common.datetimes import today
from common.interface_wfl import upLoadPhoto


# def test():
#     local a, b, c
#     try:
#         a = 1
#         b = 2
#         c = 3
#     except Exception as e:
#         a = 111
#         b = 112
#         c = 113
#     finally:
#         print a, b, c
#
# if __name__ == '__main__':
#     a = 1
#     test()
#     print a
#
li = (lambda: x for x in range(10))
li2 = [lambda: a for a in range(10)]
# print li()
print li2[0]()
#
# L = (x for x in range(10))
# # for i in li:
# #     print i()
# for l in L:
#     print l
# def my():
#     for x in range(10):
#         return x
# print my()

# def la(max):
#     i = 0
#     while i < max:
#         yield i
#         i += 1
#
# for i in la(6):
#     print i


# def test():
#     return (x for x in range(10))
#
# res = test()
# print(res)
# -*- coding:utf8 -*-

class MyClass():

    name = '123'

    def __init__(self, name):
        self.__sname = name

    @property
    def sname(self):
        return self.__sname

    @sname.setter
    def sname(self, value):
        self._sname = value

    @staticmethod
    def staticmethod():
        print 'this is staticmethon'

    @classmethod
    def classmethod(cls):
        print cls.name

    def normalmethod(self):
        print "name:'%s'" % self.name
        self.staticmethod()

if __name__ == '__main__':
    class1 = MyClass('name1')
    # class2 = MyClass('name2')
    # class3 = MyClass('name3')
    # class1.staticmethod()
    # class2.staticmethod()
    # class3.staticmethod()
    # class1.classmethod()
    # class2.classmethod()
    # class3.classmethod()
    # class1.normalmethod()
    # class2.normalmethod()
    # class3.normalmethod()

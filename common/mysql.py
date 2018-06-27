# -*- coding: UTF-8 -*-
"""
:author: wangfanglong
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import pymysql
import time
# from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from common.base import get_conf, consoleLog

class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql._getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = Mysql.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        :summary: 静态方法，从连接池中取出连接
        :return MySQLdb.connection
        """
        if Mysql.__pool is None:
            Mysql.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                                    host=get_conf('db', 'host'), port=get_conf('db', 'port', int),
                                    user=get_conf('db', 'user'), passwd=get_conf('db', 'password'),
                                    db=get_conf('db', 'db'), use_unicode=False, charset=get_conf('db', 'charset'))
                                    # cursorclass=DictCursor)  # 返回字典格式
        return Mysql.__pool.connection()

    @staticmethod
    def _convert(data):
        """
        结果数据处理
        :param data: 需要出的基础数据
        :return: 数组
        """
        if len(data) > 0:
            if type(data[0]) is tuple:
                if len(data[0]) == 1:
                    value = []
                    for i in data:
                        value.append(i[0])
                    return value
            for x, y in enumerate(data):
                if type(data[x]) is tuple or type(data[x]) is list:
                    data[x] = list(y)
                    Mysql._convert(data[x])
            return data
        else:
            return None

    @staticmethod
    def _convertUnicode(data):
        """
        转换为Unicode、int以及datetime之类的时间数据
        :param data:
        :return:
        """
        if data is None:
            return []
        else:
            for x in range(len(data)):
                if type(data[x]) is not list:
                    if type(data[x]) is not str and type(data[x]) is not int:
                        data[x] = str(data[x])
                else:
                    for y in range(len(data[x])):
                        if type(data[x][y]) is not str and type(data[x][y]) is not int:
                            data[x][y] = str(data[x][y])
            return data

    def query(self, sql, param=None, nullThrow=True, resarch=False):
        """
        返回带列名的dict数组
        :return  list,[{'contract_id':'id','house_id':'id'}]
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            index = self._cursor.description
            _result = self._cursor.fetchall()
            result = []
            for res in _result:
                row = {}
                # for key in res.keys():
                #     if type(res[key]) is not unicode and type(res[key]) is not int:
                #         res[key] = str(res[key])
                # result.append(res)
                for i in range(len(index)):
                    if type(res[i]) is not str and type(res[i]) is not int:
                        row[index[i][0]] = str(res[i])
                    else:
                        row[index[i][0]] = res[i]
                result.append(row)
            return result
        else:
            if resarch:
                for i in range(3):
                    time.sleep(3)
                    result = self.query(sql, param, nullThrow=False, resarch=False)
                    if result:
                        return result
            if nullThrow:
                raise BaseException('there is no result searched by sql: %s ' % sql)
            else:
                consoleLog('there is no result searched by sql: %s ' % sql, 'w')
                return [{}]

    def getAll(self, sql, needConvert=True, param=None, nullLog=True, research=False):
        """
        :param needConvert:
        :param research: 是否重复查询
        :param nullLog: 是否打印查询为空的日志
        :summary: 执行查询，并取出所有结果集
        :param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        :param param: 可选参数，条件列表值（元组/列表）
        :return result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
            if research:
                for i in range(3):
                    time.sleep(3)
                    result = self.getAll(sql, nullLog=False, research=False)
                    if result:
                        return result
            if nullLog:
                consoleLog(u'SQL查询为空!\nSQL:%s' % sql)
        # results_list = []
        # for i in range(len(result)):
        #     result_list = []
        #     for a in result[i].values():
        #         result_list.append(a)
        #     results_list.append(result_list)
        result = Mysql._convert(list(result))
        if needConvert:
            return Mysql._convertUnicode(result)
        else:
            return result

    def getOne(self, sql, needConvert=True, param=None, nullLog=True, research=False):
        """
        :param needConvert:
        :param research:
        :param nullLog:
        :summary: 执行查询，并取出第一条
        :param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        :param param: 可选参数，条件列表值（元组/列表）
        :return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
            if research:
                for i in range(3):
                    time.sleep(3)
                    result = self.getAll(sql, nullLog=False, research=False)
                    if result:
                        return result
            if nullLog:
                consoleLog(u'SQL查询为空!\nSQL:%s' % sql)
        result = Mysql._convert(list(result))
        if needConvert:
            return Mysql._convertUnicode(result)
        else:
            return result
        # return result

    def getMany(self, sql, num, needConvert=True, param=None, nullLog=True, research=False):
        """
        :param needConvert:
        :param research:
        :param nullLog:
        :summary: 执行查询，并取出num条结果
        :param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        :param num:取得的结果条数
        :param param: 可选参数，条件列表值（元组/列表）
        :return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
            if research:
                for i in range(3):
                    time.sleep(3)
                    result = self.getAll(sql, nullLog=False, research=False)
                    if result:
                        return result
            if nullLog:
                consoleLog(u'SQL查询为空!\nSQL:%s' % sql)
        # results_list = []
        # for i in range(len(result)):
        #     result_list = []
        #     for a in result[i].values():
        #         result_list.append(a)
        #     results_list.append(result_list)
        result = Mysql._convert(list(result))
        if needConvert:
            return Mysql._convertUnicode(result)
        else:
            return result

    def insertOne(self, sql, value):
        """
        :summary: 向数据表插入一条记录
        :param sql:要插入的ＳＱＬ格式
        :param value:要插入的记录数据tuple/list
        :return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        :summary: 向数据表插入多条记录
        :param sql:要插入的ＳＱＬ格式
        :param values:要插入的记录数据tuple(tuple)/list[list]
        :return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT ::IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        :summary: 更新数据表记录
        :param sql: ＳＱＬ格式及条件，使用(%s,%s)
        :param param: 要更新的  值 tuple/list
        :return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        :summary: 删除数据表记录
        :param sql: ＳＱＬ格式及条件，使用(%s,%s)
        :param param: 要删除的条件 值 tuple/list
        :return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        :summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        :summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        :summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

mysql = Mysql()


# if __name__ == '__main__':
#     mysql = Mysql()
#     apartment_sql = "SELECT * FROM apartment LIMIT 1"
#     results = mysql.query(apartment_sql)
#     print(results)

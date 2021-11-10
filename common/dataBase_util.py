# _*_ coding: utf-8 _*_

from pymysql import Connection
from Api_Assistant.common.configparam_util import ConfigEngine

"""
数据库sql处理封装
1、建立连接
2、创建光标
3、创建查询字符串
4、执行查询
5、提交查询
6、关闭游标
7、关闭连接
"""


class MysqlDb(object):

    def __init__(self):
        configEngine = ConfigEngine()
        self.host = configEngine.get_config('dataBase', 'host')
        self.port = configEngine.get_config('dataBase', 'port')
        self.user = configEngine.get_config('dataBase', 'user')
        self.password = configEngine.get_config('dataBase', 'password')
        self.database = configEngine.get_config('dataBase', 'database')
        self.charset = configEngine.get_config('dataBase', 'charset')

        self.conn = Connection(host=self.host,
                               port=int(self.port),
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               charset=self.charset)

        self.cursor = self.conn.cursor()

    def query_one(self, sql, params=None):
        self.cursor.execute(sql, params)

        result = self.cursor.fetchone()

        self.cursor.close()

        self.conn.close()
        return result

    def query_all(self, sql, params=None):
        self.cursor.execute(sql, params)

        results = self.cursor.fetchall()

        self.cursor.close()

        self.conn.close()

        return results

    def update(self, sql, params=None):
        self.cursor.execute(sql, params)

        self.conn.commit()

        self.cursor.close()

        self.conn.close()

    def delete(self, sql, params=None):
        self.cursor.execute(sql, params)

        self.conn.commit()

        self.cursor.close()

        self.conn.close()

    def create(self, sql, params=None):
        self.cursor.execute(sql, params)

        self.conn.commit()

        self.cursor.close()

        self.conn.close()

    def roll_back(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()

        self.conn.close()

# -*- coding: utf-8 -*-
import re
import pymysql
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import logging

class DbMysql(object):  # 继承object类所有方法

    '''
    构造方法：
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'charset':'utf8',
        'cursorclass':pymysql.cursors.DictCursor
        }
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    '''

    def __init__(self, config={}):
        if not config:
            config = {
                'host': settings['MYSQL_HOST'],
                'port': settings['MYSQL_PORT'],
                'user': settings['MYSQL_USER'],
                'passwd': settings['MYSQL_PWD'],
                'charset': 'utf8',
                'cursorclass': pymysql.cursors.DictCursor
            }
        self.debug = False
        self.host = config['host']
        self.username = config['user']
        self.password = config['passwd']
        self.port = config['port']
        self.con = None
        self.cur = None
        try:
            self.con = pymysql.connect(**config)
            self.con.autocommit(1)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except Exception as e:
            print("DataBase connect error: ",e)
            

    # 关闭数据库连接
    def close(self):
        if not self.con:
            self.con.close()
        else:
            print("DataBase doesn't connect,close connectiong error;please check the db config.")

    # 创建数据库
    def createDataBase(self, DB_NAME):
        # 创建数据库
        self.cur.execute(
            'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci' % DB_NAME)
        self.con.select_db(DB_NAME)
        print('creatDatabase:' + DB_NAME)

    # 选择数据库
    def selectDataBase(self, DB_NAME):
        self.con.select_db(DB_NAME)

    # 获取数据库版本号
    def getVersion(self):
        self.cur.execute("SELECT VERSION()")
        return self.getOneData()

    # 获取上个查询的结果
    def getOneData(self):
        # 取得上个查询的结果，是单个结果
        data = self.cur.fetchone()
        return data

    # 创建数据库表
    def creatTable(self, tablename, attrdict, constraint):
        """创建数据库表

            args：
                tablename  ：表名字
                attrdict   ：属性键值对,{'book_name':'varchar(200) NOT NULL'...}
                constraint ：主外键约束,PRIMARY KEY(`id`)
        """
        if self.isExistTable(tablename):
            print("%s is exit" % tablename)
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr, value in attrdict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s (' % tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print('creatTable:' + sql)
        self.executeCommit(sql)

    def executeSql(self, sql='', limit=1):
        """执行sql语句，针对读操作返回结果集

            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            if limit == 1:
                records = self.getOneData()
            else:
                records = self.cur.fetchall()

            return records
        except pymysql.Error as e:
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error,'\n',sql)



    def executeCommit(self, sql=''):
        """执行数据库sql语句，针对更新,删除,事务等操作失败时回滚

        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except pymysql.Error as e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print("error:", error,'\n',sql)
            return error

    def insert(self, tablename, params):
        """创建数据库表

            args：
                tablename  ：表名字
                key        ：属性键
                value      ：属性值
        """
        key = []
        value = []
        for tmpkey, tmpvalue in params.items():
            tmpkey = tablename + "." + tmpkey  # mysql8.0以上版本需要字段带上表名
            key.append(tmpkey)
            if isinstance(tmpvalue, int) or isinstance(tmpvalue, float):
                tmpvalue = str(tmpvalue)
            if isinstance(tmpvalue, str):
                tmpvalue = pymysql.escape_string(tmpvalue)
                value.append("\'" + tmpvalue + "\'")
            else:
                value.append(tmpvalue)
        attrs_sql = '(' + ','.join(key) + ')'
        values_sql = ' values(' + ','.join(value) + ')'
        sql = 'insert into %s' % tablename
        sql = sql + attrs_sql + values_sql
        if self.debug:
            print('_insert:' + sql)
        self.executeCommit(sql)

    def select(self, tablename, cond_dict='', order='', fields='*', limit=1):
        """查询数据

            args：
                tablename  ：表名字
                cond_dict  ：查询条件
                order      ：排序条件

            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                if isinstance(v, int) or isinstance(v, float):
                    v = str(v)
                v = pymysql.escape_string(v)
                consql = consql + '`' + k + '`' + '=' + '"' + v + '"' + ' and'
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                print("fields input error, please input list fields.")
        sql = sql + consql + order + "LIMIT %s" % limit
        # print(sql)
        if self.debug:
            print('select:' + sql)
        return self.executeSql(sql, limit=limit)

    def insertMany(self, table, attrs, values):
        """插入多条数据

            args：
                tablename  ：表名字
                attrs        ：属性键
                values      ：属性值

            example：
                table='test_mysqldb'
                key = ["id" ,"name", "age"]
                value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
                mydb.insertMany(table, key, value)
        """
        values_sql = ['%s' for v in attrs]
        attrs_sql = '(' + ','.join(attrs) + ')'
        values_sql = ' values(' + ','.join(values_sql) + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        if self.debug:
            print('insertMany:' + sql)
        try:
            if self.debug:
                print(sql)
            for i in range(0, len(values), 20000):
                self.cur.executemany(sql, values[i:i + 20000])
                self.con.commit()
        except pymysql.Error as e:
            self.con.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error)

    def delete(self, tablename, cond_dict):

        """删除数据

            args：
                tablename  ：表名字
                cond_dict  ：删除条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                mydb.delete(table, params)

        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                if isinstance(v, int) or isinstance(v, float):
                    v = str(v)
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where%s" % (tablename, consql)
        if self.debug:
            print(sql)
        return self.executeCommit(sql)

    def render_value_v_point(self, value):
        value = pymysql.escape_string(value)
        return value

    def update(self, tablename, attrs_dict, cond_dict):
        """更新数据

            args：
                tablename  ：表名字
                attrs_dict  ：更新属性键值对字典
                cond_dict  ：更新条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                cond_dict = {"name" : "liuqiao", "age" : "18"}
                mydb.update(table, params, cond_dict)

        """
        if not cond_dict:
            print('mysql更新条件不能为空！！！')
            return False
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            if isinstance(tmpvalue, int) or isinstance(tmpvalue, float):
                tmpvalue = str(tmpvalue)
            tmpvalue = self.render_value_v_point(tmpvalue)
            attrs_list.append("`" + tmpkey + "`" + "=" + "\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        if self.debug:
            print("attrs_sql:", attrs_sql)
        for k, v in cond_dict.items():
            if isinstance(v, int) or isinstance(v, float):
                v = str(v)
            if isinstance(v, str):
                v = "\'" + v + "\'"
            consql = consql + "`" + tablename + "`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        if self.debug:
            print(sql)
        return self.executeCommit(sql)

    def dropTable(self, tablename):
        """删除数据库表

            args：
                tablename  ：表名字
        """
        sql = "DROP TABLE  %s" % tablename
        self.executeCommit(sql)

    def deleteTable(self, tablename):
        """清空数据库表

            args：
                tablename  ：表名字
        """
        sql = "DELETE FROM %s" % tablename
        if self.debug:
            print("sql=", sql)
        self.executeCommit(sql)

    def isExistTable(self, tablename):
        """判断数据表是否存在

            args：
                tablename  ：表名字

            Return:
                存在返回True，不存在返回False
        """
        sql = "select * from %s" % tablename
        result = self.executeCommit(sql)
        if result is None:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True

# if __name__ == "__main__":
#
#     # 定义数据库访问参数
#     config = {
#         'host': '127.0.0.1',
#         'port': 6806,
#         'user': 'root',
#         'passwd': 'tcltest',
#         'charset': 'utf8',
#         'cursorclass': pymysql.cursors.DictCursor
#     }
#
#     # 初始化打开数据库连接
#     mydb = DbMysql(config)
#
#     # 打印数据库版本
#     print(mydb.getVersion())
#
#     # 创建数据库
#     DB_NAME = 'test_db'
#     # mydb.createDataBase(DB_NAME)
#
#
#     # 选择数据库
#     print("========= 选择数据库%s ===========" % DB_NAME)
#     mydb.selectDataBase(DB_NAME)
#
#     #创建表
#     TABLE_NAME = 'test_user'
#     print("========= 选择数据表%s ===========" % TABLE_NAME)
#     # CREATE TABLE %s(id int(11) primary key,name varchar(30))' %TABLE_NAME
#     attrdict = {'name':'varchar(30) NOT NULL'}
#     constraint = "PRIMARY KEY(`id`)"
#     # mydb.creatTable(TABLE_NAME,attrdict,constraint)
#
#     # 插入纪录
#     print("========= 单条数据插入 ===========")
#     params = {}
#     for i in range(5):
#         params.update({"name":"testuser"+str(i)}) # 生成字典数据，循环插入
#         print(params)
#         mydb.insert(TABLE_NAME, params)
#         print("")
#
#     # 批量插入数据
#     print("========= 多条数据同时插入 ===========")
#     insert_values = []
#     for i in range(5):
#         # values.append((i,"testuser"+str(i)))
#         insert_values.append([u"测试用户"+str(i)]) # 插入中文数据
#     print(insert_values)
#     insert_attrs = ["name"]
#     mydb.insertMany(TABLE_NAME,insert_attrs, insert_values)
#
#     # 数据查询
#     print("========= 数据查询 ===========")
#     print(mydb.select(TABLE_NAME, fields=["id", "name"]))
#     print(mydb.select(TABLE_NAME, cond_dict    = {'name':'测试用户2'},fields=["id", "name"]))
#     print(mydb.select(TABLE_NAME, cond_dict = {'name':'测试用户2'},fields=["id", "name"],order="order by id desc"))
#
#     # 删除数据
#     print("========= 删除数据 ===========")
#     delete_params = {"name": "测试用户2"}
#     mydb.delete(TABLE_NAME, delete_params)
#
#     # 更新数据
#     print("========= 更新数据 ===========")
#     update_params = {"name": "测试用户99"}   # 需要更新为什么值
#     update_cond_dict = {"name": "测试用户3"}  # 更新执行的查询条件
#     mydb.update(TABLE_NAME, update_params, update_cond_dict)
#
#     # 删除表数据
#     print("========= 删除表数据 ===========")
#     mydb.deleteTable(TABLE_NAME)
#
#     # 删除表
#     print("========= 删除表     ===========")
#     mydb.dropTable(TABLE_NAME)

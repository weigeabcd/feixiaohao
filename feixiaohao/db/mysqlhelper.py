# -*- coding: utf-8 -*-
import sys
sys.path.append(r"/data/coin-library/py_spider/coin/feixiaohao/")
from feixiaohao.db.DbMysql import DbMysql
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import pymysql

class MysqlHelper(object):
    def __init__(self,config={}):
        # 实例化mysql
        self.db_store = ''
        if not config:
            config = {
                'host': settings['MYSQL_HOST'],
                'port': settings['MYSQL_PORT'],
                'user': settings['MYSQL_USER'],
                'passwd': settings['MYSQL_PWD'],
                'charset': 'utf8',
                'cursorclass': pymysql.cursors.DictCursor,
                'db': settings['MYSQL_DATA_DB']
            }
        mydb = DbMysql(config)
        DB_NAME = config['db']
        mydb.selectDataBase(DB_NAME)
        self.mydb = mydb

    def dbSave(self, tableName=None, item={}):
        self.mydb.insert(tablename=tableName, params=item)

    def dbUpdate(self, tableName=None, item={}, where={}):
        self.mydb.update(tablename=tableName, attrs_dict=item, cond_dict=where)

    def dbDelete(self, tableName=None, where={}):
        self.mydb.delete(tablename=tableName, cond_dict=where)

    def dbGet(self, tableName=None, where={}, fields=['*'], limit=1):
        rows = self.mydb.select(tablename=tableName, cond_dict=where, fields=fields, limit=limit)
        return rows

    def custom_dbGet(self,sql='',limit=1):
        rows = self.mydb.executeSql(sql,limit)
        return rows


if __name__ == "__main__":
    config = {
        'host': '192.168.1.140',
        'port': 3306,
        'user': 'root',
        'passwd': 'xiaoma',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
        'db':'coin_detail'
    }
    db = MysqlHelper(config=config)
    # sql = 'SELECT * FROM s3_appleid'
    # res = db.custom_dbGet(sql,limit=0)
    # print(res)




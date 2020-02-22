# -*- coding: utf-8 -*-
import json
import requests
import sys
sys.path.append(r"/data/coin-library/py_spider/coin/feixiaohao/")
from feixiaohao.db.mysqlhelper import MysqlHelper
from feixiaohao.tools import common
DB = MysqlHelper()
import pymysql
from feixiaohao import settings
from feixiaohao import items

def get_code():
    tableName = "spider_coin_record"
    mysql_db_detail = MysqlHelper(config={
        'host': settings.MYSQL_HOST,
        'port': settings.MYSQL_PORT,
        'user': settings.MYSQL_USER,
        'passwd': settings.MYSQL_PWD,
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
        'db': 'coin_detail'
    })
    return mysql_db_detail.dbGet(tableName=tableName, where={'disable': 0},fields=[tableName + '.id', tableName + '.slug', ], limit=100000)


def parse(restexts,spider_coin_record_id):
    json_text = json.loads(restexts)
    data_list = json_text["data"]
    for data in data_list:
        event_item = items.eventItem()
        event_item["spider_coin_record_id"]=spider_coin_record_id
        event_item["eventdate"]=data["eventdate"]
        event_item["title"]=data["title"]
        duplicate_item = {
            "md5": common.md5str(str(event_item))
        }
        res = DB.dbGet("duplicate", duplicate_item, ["id"])
        if not res:
            print(event_item,"插入新的事件消息")
            DB.dbSave('duplicate', duplicate_item)
            DB.dbSave('event', event_item)



def main():
    spider_list = get_code()
    for spider in spider_list:
        slug = spider["slug"]
        spider_coin_record_id = spider["id"]
        url = "https://dncapi.bqiapp.com/api/v2/coin/bigevent?coincode=%s&webp=1" % slug
        restexts = common._request(url,"get",{"User-Agent":common.get_randomUa()})
        parse(restexts,spider_coin_record_id)

        # break



if __name__=="__main__":
    main()


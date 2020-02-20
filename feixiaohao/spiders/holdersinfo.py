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

def get_data(slug):
    url = "https://dncapi.bqiapp.com/api/v3/coin/holders?code=%s&webp=1" % slug
    try:
        headers={
            "User-Agent":common.get_randomUa()
        }
        r = requests.get(url=url,headers=headers)
        if r.status_code==200:
            # print(r.text)
            return r.text
        else:
            print("错误的状态码：{}".format(r.status_code))
            return False
    except Exception as e:
        print(e)
        return False

def parse_data(text,spider_coin_record_id):
    # data_item ={}
    json_text = json.loads(text)
    # print(json_text)
    toplist = json_text["data"]["toplist"]
    for rank,top in enumerate(toplist):
        updatetime = top["updatetime"].replace("T"," ").strip("Z")
        # print(updatetime)
        updatetime = common.timestamp(updatetime)
        infoItem={}
        infoItem["spider_coin_record_id"]=spider_coin_record_id
        infoItem["address"]=top["address"]
        infoItem["quantity"]=top["quantity"]
        infoItem["percentage"]=top["percentage"]
        infoItem["updatetime"]=updatetime
        infoItem["rank"]=rank+1
        print(infoItem)
        db_table="holdersinfo"
        DB.dbSave(db_table,infoItem)



def main():
    spider_list = get_code()
    for spider in spider_list:
        slug = spider["slug"]
        spider_coin_record_id = spider["id"]
        text = get_data(slug)
        if text:
            parse_data(text,spider_coin_record_id)

        # break

main()











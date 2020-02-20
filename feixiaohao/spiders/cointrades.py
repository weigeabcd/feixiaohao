# -*- coding: utf-8 -*-
import json
import requests
import sys
sys.path.append(r"/data/coin-library/py_spider/coin/feixiaohao/")
from feixiaohao.db.mysqlhelper import MysqlHelper
from feixiaohao.tools import common
from feixiaohao import settings
import pymysql
DB = MysqlHelper()


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
    return mysql_db_detail.dbGet(tableName=tableName, where={'disable': 0},fields=[tableName + '.id', tableName + '.slug' ], limit=100000)

def get_data(slug):
    url = "https://dncapi.bqiapp.com/api/coin/cointrades-web?code=%s&webp=1" % slug
    try:
        headers = {
            "User-Agent": common.get_randomUa()
        }
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            # print(r.text)
            return r.text
        else:
            print("错误的状态码：{}".format(r.status_code))
            return False
    except Exception as e:
        print(e)
        return False

def parse_data(text,spider_coin_record_id):
    data_item ={}
    json_text = json.loads(text)
    datalist = json_text["data"]
    for data in datalist:
        # print(data)
        data_item["spider_coin_record_id"] = spider_coin_record_id
        data_item["name"] = data["name"]
        data_item["percent"] = data["percent"]
        # print(data_item)
        table = "cointrades"
        res = DB.dbGet(table,{"spider_coin_record_id":spider_coin_record_id,"name":data["name"]},["id"])
        if res:
            print(data_item,"已存在，更新")
            cointrades_id = res["id"]
            DB.dbUpdate(table,data_item,{"id":cointrades_id})
        else:
            print(data_item,"不存在---插入！！！")
            DB.dbSave(table,data_item)


def main():
    spider_coin_list = get_code()
    # print(len(spider_coin_list))
    for spider_coin in spider_coin_list:
        slug = spider_coin['slug']
        # slug = "bitcoin"  # test
        spider_coin_record_id = spider_coin['id']
        text = get_data(slug)
        if text:
            parse_data(text, spider_coin_record_id)
        # break

main()

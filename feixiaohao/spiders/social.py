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
    url = "https://dncapi.bqiapp.com/api/v3/coin/hotsocial?coincode=%s&webp=1" % slug
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
    updatedate = json_text["data"]["social"]["updatedate"]
    if updatedate == 0:
        print(json_text)
    else:
        social_item = json_text["data"]["social"]
        for k,v in social_item.items():
            if "--" in str(v):
                v = v.replace("--","")
            if v:
                if k=="updatedate":
                    v = str(v)[0:4]+"-"+str(v)[4:6]+"-"+str(v)[6:8]
                social_item[k] = v
        social_item["spider_coin_record_id"] = spider_coin_record_id
        table = "social"
        res = DB.dbGet(table,{"spider_coin_record_id":spider_coin_record_id},["id"])
        if res:
            print(spider_coin_record_id,"已存在，更新原数据")
            social_id = res["id"]
            DB.dbUpdate(table,social_item,{"id":social_id})
        else:
            DB.dbSave(table,social_item)
        print(social_item)

def main():
    spider_list = get_code()
    for spider in spider_list:
        slug = spider["slug"]
        spider_coin_record_id = spider["id"]
        text = get_data(slug)
        if text:
            parse_data(text,spider_coin_record_id)

        # break

if __name__=="__main__":
    main()










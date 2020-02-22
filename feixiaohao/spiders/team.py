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
    team_list = json_text["data"]["team"]
    for team in team_list:
        dataItem = items.teamItem()
        dataItem["spider_coin_record_id"]=spider_coin_record_id
        for k,v in team.items():
            if v:
                if k == "description":
                    v = common.remove_tag(v)
                dataItem[k]=v
        select_item={
            "spider_coin_record_id":spider_coin_record_id,
            "code":dataItem["code"]
        }
        team_tb = "team"
        dbres = DB.dbGet(team_tb,select_item,["id"])
        if dbres:
            print(select_item,"更新")
            dbres_id = dbres["id"]
            DB.dbUpdate(team_tb,dataItem,{"id":dbres_id})
        else:
            DB.dbSave(team_tb,dataItem)
        # print(dataItem)

def main():
    spider_list = get_code()
    for spider in spider_list:
        slug = spider["slug"]
        spider_coin_record_id = spider["id"]
        url = "https://dncapi.bqiapp.com/api/v3/coin/team?code=%s&webp=1" % slug
        restexts = common._request(url,"get",{"User-Agent":common.get_randomUa()})
        parse(restexts,spider_coin_record_id)

        # break


if __name__=="__main__":
    main()

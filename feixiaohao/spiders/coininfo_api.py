# -*- coding: utf-8 -*-
import json
import requests
import sys
sys.path.append(r"/data/coin-library/py_spider/coin/feixiaohao/")
from feixiaohao.db.mysqlhelper import MysqlHelper
from feixiaohao.tools import common
from feixiaohao.tools import clear
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
    return mysql_db_detail.dbGet(tableName=tableName, where={'disable': 0},fields=[tableName + '.id', tableName + '.slug'], limit=100000)

def get_data(slug):
    url = 'https://dncapi.bqiapp.com/api/coin/web-coininfo'
    payload = {'code': slug}
    headers = {'content-type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            # print(r.text)
            return r.text
        else:
            return False
    except:
        print(slug,"请求失败")
        return False

def parse_data(text,spider_coin_record_id,slug):
    data_item ={}
    json_text = json.loads(text)
    data = json_text['data']
    if data:
        siteurl = data["siteurl"]
        siteurl = siteurl.replace("\n",";") if siteurl else ''
        white_paper = data["white_paper"]
        white_paper = white_paper.replace("\n", ";") if siteurl else ''
        coindesc = data["coindesc"]
        coindesc = clear.get_coin_about(coindesc)
        coindesc = common.remove_tag(coindesc).replace("*以上内容由非小号官方整理，如若转载，请注明出处。","").replace("\n",'').replace("\xa0",'').strip() if coindesc else ""
        data_item["id"]=spider_coin_record_id
        data_item["slug"]=slug
        data_item["name"]=data["name"]
        data_item["chinese_name"]=data["name_zh"]
        data_item["short_name"]=data["symbol"]
        data_item["logo_url"]=data["logo"]
        data_item["online_time"]=data["online_time"].replace("--","")
        data_item["maxsupply"]=data["maxsupply"]
        data_item["Website"]=siteurl
        data_item["mechanism"]=data["prooftype"]
        data_item["algorithm"]=data["algorithm"]
        data_item["Technical_Documentation"]=white_paper
        data_item["About"]=coindesc
        # print(data_item)
        table = "coin_basic"
        res = DB.dbGet(table,{"id":spider_coin_record_id},["id"])
        if res:
            print(slug,"已存在基础表，更新")
            data_item.pop("logo_url")
            data_item.pop("About")
            DB.dbUpdate(table,data_item,{"id":spider_coin_record_id})
        else:
            print(slug, "bu不bu存在基础表，插入")
            DB.dbSave(table,data_item)
    else:
        print(text)

def main():
    spider_coin_list = get_code()
    # print(len(spider_coin_list))
    for spider_coin in spider_coin_list:
        slug = spider_coin['slug']
        # slug = "bitcoin"  # test
        spider_coin_record_id = spider_coin['id']
        text = get_data(slug)
        if text:
            parse_data(text, spider_coin_record_id,slug)

        # break

main()

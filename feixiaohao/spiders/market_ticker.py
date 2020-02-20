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
base_url = "https://dncapi.bqiapp.com/api/coin/market_ticker?page=%s&pagesize=100&code=%s&token=&tickertype=0&pair2=&webp=1"
# all_markets_list = []

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

def requests_get(url):
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

def get_and_parse_data(slug,spider_coin_record_id,page=1):
    url = base_url % (str(page), slug)
    print("开始请求：{}".format(url))
    text = requests_get(url)
    if text:
        json_text = json.loads(text)
        markets_list = json_text["data"]["markets"]
        # print(markets_list)
        if markets_list:
            for markets in markets_list:
                print(markets)
                data_item = {}
                name = markets["name"]
                percent = markets["accounting"]
                if percent > 0:
                    data_item["spider_coin_record_id"] = spider_coin_record_id
                    data_item["name"] = name
                    data_item["percent"] = percent
                    print(data_item)
                    # table = "exchange_proportion"
                    # res = DB.dbGet(table, {"spider_coin_record_id": spider_coin_record_id, "name": name}, ["id"])
                    # if res:
                    #     print(data_item, "已存在，更新~~~")
                    #     cointrades_id = res["id"]
                    #     DB.dbUpdate(table, data_item, {"id": cointrades_id})
                    # else:
                    #     print(data_item, "不存在---插入！！！")
                    #     DB.dbSave(table, data_item)
                # print(data_item)

            # 请求下一页，直到markets_list为空
            # page +=1
            # return get_and_parse_data(slug,spider_coin_record_id,page)
        else:
            if page == 1:
                print(slug,"没有交易所占比信息")
            else:
                print(slug,"交易所占比信息请求完成")

def main():
    spider_coin_list = get_code()
    # print(len(spider_coin_list))
    for spider_coin in spider_coin_list:
        slug = spider_coin['slug']
        # slug = "bitcoin"  # test
        spider_coin_record_id = spider_coin['id']
        get_and_parse_data(slug,spider_coin_record_id)



        break
main()

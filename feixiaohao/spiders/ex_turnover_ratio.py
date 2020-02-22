# -*- coding: utf-8 -*-
import json
import sys
sys.path.append(r"/data/coin-library/py_spider/coin/feixiaohao/")
from feixiaohao.db.mysqlhelper import MysqlHelper
from feixiaohao.tools import common
DB = MysqlHelper()
import pymysql
from feixiaohao import settings




def main():
    slug = "binance"
    url = "https://dncapi.bqiapp.com/api/exchange/coinpair_list"
    headers = {'content-type': 'application/json',"User-Agent":common.get_randomUa()}
    dataItem = {
        "page":1,
        "code":slug,
        "pagesize":100,
    }
    data = json.dumps(dataItem)
    res_text = common._request(url,"post",headers,data)
    json_text = json.loads(res_text)
    datalist = json_text["data"]
    for data in datalist:
        print(data)
        coincode = data["coincode"]
        symbol_pair = data["symbol_pair"]
        price = data["price"]
        volume = data["volume"]
        accounting = data["accounting"]
        update_time = data["update_time"]
        print(coincode,symbol_pair,price,volume,accounting,update_time)


main()





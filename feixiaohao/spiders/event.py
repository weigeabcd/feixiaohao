# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from feixiaohao.db.mysqlhelper import MysqlHelper
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import pymysql
import logging
import json
from feixiaohao import items

class EventSpider(Spider):
    name = 'event'
    allowed_domains = ['dncapi.bqiapp.com']
    start_urls = ['http://dncapi.bqiapp.com/']

    def __init__(self):
        self.mysql_db = MysqlHelper()
        self.event_api = "https://dncapi.bqiapp.com/api/v2/coin/bigevent?coincode=%s&webp=1"
        self.mysql_db_detail = MysqlHelper(config={
            'host': settings['MYSQL_HOST'],
            'port': settings['MYSQL_PORT'],
            'user': settings['MYSQL_USER'],
            'passwd': settings['MYSQL_PWD'],
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
            'db': 'coin_detail'
        })

    def start_requests(self):
        # 从小马本地数据库获取最新的任务表
        tableName = "spider_coin_record"
        xiaoma_dbres_list = self.mysql_db_detail.dbGet(tableName=tableName, where={'disable': 0},fields=[tableName + '.id', tableName + '.slug',], limit=100000)
        for xiaoma_dbres in xiaoma_dbres_list:
            slug = xiaoma_dbres['slug']
            # slug = "bitcoin"  # test
            spider_coin_record_id = xiaoma_dbres['id']
            url = self.event_api % slug
            yield Request(url=url, callback=self.parse, meta={'spider_coin_record_id': spider_coin_record_id})

            # break
    def parse(self, response):
        meta = response.meta
        spider_coin_record_id = meta["spider_coin_record_id"]
        json_text = json.loads(response.text)
        data_list = json_text["data"]
        for data in data_list:
            event_item = items.eventItem()
            event_item["spider_coin_record_id"] = spider_coin_record_id
            event_item["eventdate"] = data["eventdate"]
            event_item["title"] = data["title"]
            # print(event_item)
            yield event_item





# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from feixiaohao.db.mysqlhelper import MysqlHelper
from feixiaohao import items
import logging
import json
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import pymysql

class TeamSpider(Spider):
    name = 'team'
    allowed_domains = ['dncapi.bqiapp.com']
    start_urls = ['http://dncapi.bqiapp.com/']

    def __init__(self):
        self.mysql_db = MysqlHelper()
        self.team_api = "https://dncapi.bqiapp.com/api/v3/coin/team?code=%s&webp=1"
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
            dbres = self.mysql_db.dbGet('team', {'spider_coin_record_id': spider_coin_record_id}, ['id'])
            if not dbres:
                # print(slug,'基础数据不存在，爬取！！')
                url = self.team_api % slug
                yield Request(url=url, callback=self.parse, meta={'spider_coin_record_id': spider_coin_record_id})
            else:
                logging.info(slug + " 已存在，不需要请求爬取")

            # break

    def parse(self, response):
        meta = response.meta
        spider_coin_record_id = meta["spider_coin_record_id"]
        json_text = json.loads(response.text)
        team_list = json_text["data"]["team"]
        if team_list:
            for team in team_list:
                team_item_loader = items.teamItemLoader(item=items.teamItem(), response=response)
                for k,v in team.items():
                    if v:
                        team_item_loader.add_value(k,v)
                team_item_loader.add_value('spider_coin_record_id',spider_coin_record_id)
                team_item = team_item_loader.load_item()
                # print(team_item)
                yield team_item
        # else:
        #     print(response.url,"没有团队信息",spider_coin_record_id)




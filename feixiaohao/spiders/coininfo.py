# -*- coding: utf-8 -*-
from scrapy import Spider,FormRequest,Request
from feixiaohao.db.mysqlhelper import MysqlHelper
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import pymysql
import logging
# import json
from feixiaohao import items
from feixiaohao.tools import common


class CoininfoSpider(Spider):
    name = 'coininfo'
    allowed_domains = ['dncapi.bqiapp.com']
    start_urls = ['http://dncapi.bqiapp.com/']

    def __init__(self):
        self.mysql_db = MysqlHelper()
        self.info_api = "https://dncapi.bqiapp.com/api/coin/web-coininfo"
        self.info_url = "https://www.feixiaohao.com/currencies/%s/"
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
        xiaoma_dbres_list = self.mysql_db.dbGet(tableName=tableName, where={'disable': 0},fields=[tableName + '.id', tableName + '.slug',], limit=100000)
        for xiaoma_dbres in xiaoma_dbres_list:
            slug = xiaoma_dbres['slug']
            # slug = "bitcoin"  # test
            spider_coin_record_id = xiaoma_dbres['id']
            dbres = self.mysql_db.dbGet('coininfo', {'spider_coin_record_id': spider_coin_record_id}, ['id'])
            if not dbres:
                # print(slug,'基础数据不存在，爬取！！')
                # form_data = {"code":slug}
                yield Request(url=self.info_url % slug,meta={'spider_coin_record_id':spider_coin_record_id,"slug":slug},callback=self.parse)
            else:
                logging.info(slug + " 已存在，不需要请求爬取")

            # break

    def parse(self, response):
        meta = response.meta
        spider_coin_record_id = meta["spider_coin_record_id"]
        slug = meta["slug"]
        title_list = response.css(".infoList_new .tit::text").extract()
        value_list = response.css(".infoList_new .val::text").extract()
        info_list_item = {}
        for tit_i,tit in enumerate(title_list):
            tit = tit.strip()
            if tit == "发行时间" or tit == "最大供应量" or tit == "激励机制":
                info_list_item[tit] = value_list[tit_i]

        url_tit_list = response.css(".infoList .tit::text").extract()
        url_val_list = response.css(".infoList .val")
        url_info_list_item = {}
        for i,v in enumerate(url_tit_list):
            if v == "官网地址" or v == "白皮书":
                url_info_list_item[v] = url_val_list[i]
        siteurl=''
        white_paper=''
        web_css = common.get_value_from_item("官网地址",url_info_list_item)
        if web_css:
            siteurl = ';'.join(web_css.css("a::attr(href)").extract())
        bps_css = common.get_value_from_item("白皮书",url_info_list_item)
        if bps_css:
            white_paper = ';'.join(bps_css.css("a::attr(href)").extract())

        coin_item_loader = items.coininfoItemLoader(item=items.coininfoItem(),response=response)
        coin_item_loader.add_value("spider_coin_record_id",spider_coin_record_id)
        coin_item_loader.add_css("name",".main h1 small::text")
        coin_item_loader.add_css("name_zh",".main h1::text")
        coin_item_loader.add_css("symbol",".main h1::text")
        coin_item_loader.add_css("logo",".title img::attr(src)")
        coin_item_loader.add_css("coindesc",".textBox::text")
        coin_item_loader.add_value("online_time",common.get_value_from_item("发行时间",info_list_item))
        coin_item_loader.add_value("maxsupply",common.get_value_from_item("最大供应量",info_list_item))
        coin_item_loader.add_value("mechanism",common.get_value_from_item("激励机制",info_list_item))
        coin_item_loader.add_value("siteurl",siteurl)
        coin_item_loader.add_value("white_paper",white_paper)
        coin_item = coin_item_loader.load_item()
        print(coin_item)
        yield coin_item







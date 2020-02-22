# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from feixiaohao import items
from feixiaohao.db.mysqlhelper import MysqlHelper
# import requests
from feixiaohao.tools import common
# import os
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
# import logging
from feixiaohao.tools import common

class logo_downloader(object):
    '''图片下载器'''
    def __init__(self):
        self.team_members = settings['TEAM_MEMBER']

    def process_item(self, item, spider):
        if isinstance(item, items.teamItem):
            code = item['code']
            logo_url = common.get_value_from_item("logo",item)
            if logo_url:
                iconname = self.team_members + code + '.png'
                # print(iconname)
                common.dowmloaderfile(iconname,logo_url)
                item['logo'] = iconname

        return item

class MysqlPipeline(object):
    '''数据存储器'''
    def __init__(self):
        self.mysql_db = MysqlHelper()

    def process_item(self, item, spider):
        if isinstance(item, items.teamItem):
            table = 'team'
            self.mysql_db.dbSave(table,item)

        elif isinstance(item, items.eventItem):
            duplicate_item={
                "md5":common.md5str(str(item))
            }
            res = self.mysql_db.dbGet("duplicate",duplicate_item,["id"])
            if not res:
                self.mysql_db.dbSave('duplicate',duplicate_item)
                self.mysql_db.dbSave('event',item)
            # else:
            #     print(item,"已存在")
        elif isinstance(item, items.coininfoItem):
            table = 'coininfo'
            self.mysql_db.dbSave(table,item)
        return item





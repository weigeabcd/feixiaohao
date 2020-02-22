# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader, wrap_loader_context
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.utils.datatypes import MergeDict
from scrapy.utils.misc import arg_to_iter
from feixiaohao.tools import common
from feixiaohao.tools import clear

##########全局重写###########
class MapComposeCustom(MapCompose):
    # 自定义MapCompose，当value没元素时传入" "
    def __call__(self, value, loader_context=None):
        if isinstance(value, list):
            if not value:
                value.append(" ")
            value = value[0]
        values = arg_to_iter(value)
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        for func in wrapped_funcs:
            next_values = []
            for v in values:
                next_values += arg_to_iter(func(v))
            values = next_values
        return values

class TakeFirstCustom(TakeFirst):
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value.strip() if isinstance(value, str) else value
            else:
                return ""
##########全局重写###########

class commonItemLoader(ItemLoader):
    """这是公用的ItemLoader"""
    default_output_processor = TakeFirstCustom()

# class teamItemLoader(commonItemLoader):
#     """这是teamItemLoader"""
#     description_in = MapComposeCustom(common.remove_tag)

class teamItem(Item):
    """这是teamItem"""
    spider_coin_record_id = Field()
    code = Field()
    description = Field()
    intro = Field()
    linkinlink = Field()
    logo = Field()
    name = Field()
    nativename = Field()
    twitterlink = Field()

class eventItem(Item):
    spider_coin_record_id = Field()
    eventdate = Field()
    title = Field()

class coininfoItemLoader(commonItemLoader):
    """这是coininfoItem字段加载器"""
    coindesc_in = MapComposeCustom(clear._coindesc)
    maxsupply_in = MapComposeCustom(clear._maxsupply)
    name_zh_in = MapComposeCustom(clear._name_zh)
    symbol_in = MapComposeCustom(clear._symbol)

class coininfoItem(Item):
    """这是coinItem"""
    spider_coin_record_id = Field()
    name = Field()
    name_zh = Field()
    symbol = Field()
    logo = Field()
    online_time = Field()
    maxsupply = Field()
    siteurl = Field()
    if_collect = Field()
    if_dig = Field()
    mechanism = Field()
    white_paper = Field()
    coindesc = Field()






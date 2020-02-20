# -*- coding: utf-8 -*-
import re

def _coindesc(v):
    return v.replace("\xa0"," ").replace("*以上内容由非小号官方整理，如若转载，请注明出处。",'')

def _maxsupply(v):
    list = re.findall("\d+",v)
    if list:
        return ''.join(list)
    else:
        return 0

def _name_zh(v):
    if "," in v:
        return v.split(",")[1]
    else:
        return ''

def _symbol(v):
    if ',' in v:
        return v.split(",")[0]
    else:
        return ''

def get_coin_about(v):
    if "<hr />" in v:
        return v.split("<hr />")[0]
    else:
        return v

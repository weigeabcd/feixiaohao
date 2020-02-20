# -*- coding: utf-8 -*-
from hashlib import md5
from fake_useragent import UserAgent
import requests
import os
import base64
import time
import re
from w3lib.html import remove_tags

def md5str(s):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()

def remove_tag(value):
    return remove_tags(value)

def get_randomUa():
    ua = UserAgent()
    return ua.random

def dowmloaderfile(filename,res_url):
    # print(headers)
    if not os.path.exists(filename):
        try:
            headers = {'user-agent': get_randomUa(), }
            pic = requests.get(res_url, headers=headers, timeout=10)
            fp = open(filename, 'wb')
            fp.write(pic.content)
            fp.close()
            return True
        except:
            print(res_url,"文件下载失败！！！！！！")
            # ip失效，更换代理
            return False
    else:
        print(filename, '文件存在，不下载')
        return True

def get_value_from_item(key,item):
    try:
        return item[key]
    except:
        return ''

def base64_encode_str(value):
    bytes_url = value.encode("utf-8")
    return base64.b64encode(bytes_url).decode(encoding = "utf-8")

def get_not_int_time():
    return int(time.time())

def timestamp(timeformat=None, format='%Y-%m-%d %H:%M:%S'):
    if timeformat:
        time_tuple = time.strptime(timeformat, format)
        res = time.mktime(time_tuple)  # 转成时间戳
    else:
        res = time.time()  # 获取当前时间戳
    return int(res)

def format_time_to_int_time(timestr='', have_hms=False):
    timestr = timestr.strip()
    if timestr:
        if have_hms:
            format = '%Y-%m-%d %H:%M:%S'
        else:
            format = "%Y-%m-%d"
        time_string = convert_time_for_ymdhis(timestr, have_hms)
        time_int = timestamp(time_string, format)
        return time_int
    else:
        return 0

def convert_time_for_ymdhis(value, have_hms=False):
    list = get_number_from_string(value, True)
    # real_string_time = ''
    _year = '2019'
    _sec = '00'
    _min = '00'
    _hour = '00'
    _day = '01'
    _month = '01'
    if len(list) >= 1:
        _year = list[0]
    if len(list) >= 2:
        _month = list[1]
    if len(list) >= 3:
        _day = list[2]
    if len(list) >= 4:
        _hour = list[3]
    if len(list) >= 5:
        _min = list[4]
    if len(list) >= 6:
        _sec = list[5]
    if have_hms:
        real_string_time = "{0}-{1}-{2} {3}:{4}:{5}".format(_year, _month, _day, _hour, _min, _sec)
    else:
        real_string_time = "{0}-{1}-{2}".format(_year, _month, _day, _hour, _min, _sec)
    return real_string_time

def get_number_from_string(str, is_list=False):
    """从字符串中提取数组"""
    number = re.findall(r'\d+', str)
    if is_list:
        return number
    number = "".join(number)
    return number

def _request(url='',methods="get",headers={},dataItem={}):
    if not url:
        print("url不能为空")
        return
    if methods == "get":
        try:
            r = requests.get(url=url, headers=headers)
            if r.status_code == 200:
                return r.text
            else:
                print("错误的状态码：{}".format(r.status_code))
                return False
        except Exception as e:
            print(e)
            return False
    elif methods == "post":
        if not dataItem:
            print("dataItem不能为空")
            return
        try:
            r = requests.post(url=url,data=dataItem,headers=headers)
            if r.status_code==200:
                return r.text
            else:
                print("错误的状态码：{}".format(r.status_code))
                return False
        except Exception as e:
            print(e)
            return False

if __name__=="__main__":
    a = '2020-01-13 00:00:00'
    res = md5str(a)
    print(res)
    # print(time.time())





# -*- coding: utf-8 -*-

# Scrapy settings for feixiaohao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'feixiaohao'

SPIDER_MODULES = ['feixiaohao.spiders']
NEWSPIDER_MODULE = 'feixiaohao.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'feixiaohao (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'feixiaohao.middlewares.FeixiaohaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'feixiaohao.middlewares.RandomUserAgent': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
   # 'feixiaohao.pipelines.logo_downloader': 300,
   'feixiaohao.pipelines.MysqlPipeline': 301,
}

# 重试次数
RETRY_TIMES = 4
# 下载延迟
DOWNLOAD_DELAY = 1
# 下载超时时长
DOWNLOAD_TIMEOUT = 60

import datetime
to_day = datetime.datetime.now()
TEST = 2
if TEST==1:
    # myself本地测试数据库
    MYSQL_HOST = "127.0.0.1"
    MYSQL_USER = "root"
    MYSQL_PWD = "Dd112211"
    MYSQL_DATA_DB = "coin_detail"
    MYSQL_PORT = 3306
    ICON_PATH = 'D:/python_app/scrapy_app/bees_check/icon/'
    EXCHANGE_PATH = 'D:/python_app/scrapy_app/bees_check/exchange/'
    TEAM_MEMBER = 'D:/python_app/scrapy_app/bees_check/team_members/'
    # 日志等级
    LOG_LEVEL = "DEBUG"
elif TEST==2:
    # 小马本地数据库
    MYSQL_HOST = "192.168.1.140"
    MYSQL_USER = "root"
    MYSQL_PWD = "xiaoma"
    MYSQL_DATA_DB = "coin_library"
    MYSQL_PORT = 3306
    ICON_PATH = '/data/coin-library/py_spider/coin/icon/'
    EXCHANGE_PATH = '/data/coin-library/py_spider/coin/exchange/'
    TEAM_MEMBER = '/data/coin-library/py_spider/coin/team_members/'
    # 日志等级
    LOG_LEVEL = "DEBUG"
    # LOG_FILE = "/data/logs/feixiaohao/team_{}_{}_{}.log".format(to_day.year,to_day.month,to_day.day)











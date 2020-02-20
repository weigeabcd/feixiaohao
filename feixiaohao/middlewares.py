from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import time
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from urllib3.exceptions import ProtocolError, ProxyError, ProxySchemeUnknown
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from feixiaohao.tools import common

class RandomUserAgent(object):
    def process_request(self, request, spider):
        ua = common.get_randomUa()
        # print(ua)
        request.headers['User-Agent'] = ua
        # request.headers['Encoding'] = 'utf-8'

class TooManyRequestsRetryMiddleware(RetryMiddleware):
    """重写了retry中间件，太多请求被限制时，爬虫等待一分钟再执行"""
    def __init__(self, crawler):
        super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler
        self.retry_http_codes = settings['RETRY_HTTP_CODES']
        self.EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                                    ConnectionRefusedError, ConnectionDone, ConnectError,
                                    ConnectionLost, TCPTimedOutError, ResponseFailed,
                                    IOError, TunnelError, ProtocolError, ProxyError, ProxySchemeUnknown)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        # elif response.status == 429:
        #     print('429状态码，爬虫等待70秒')
        #     self.crawler.engine.pause() # 暂停爬虫引擎
        #     time.sleep(70) # If the rate limit is renewed in a minute, put 60 seconds, and so on.
        #     self.crawler.engine.unpause() # 恢复爬虫引擎
        #     reason = response_status_message(response.status)
        #     return self._retry(request, reason, spider) or response
        elif response.status in self.retry_http_codes:
            print('429状态码，爬虫等待100秒')
            self.crawler.engine.pause()  # 暂停爬虫引擎
            time.sleep(100)  # If the rate limit is renewed in a minute, put 60 seconds, and so on.
            self.crawler.engine.unpause()  # 恢复爬虫引擎
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)





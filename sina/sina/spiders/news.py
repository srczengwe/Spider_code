# -*- coding: utf-8 -*-
# import scrapy

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis.spiders import RedisSpider
from sina.items import SinaItem


class NewsSpider(RedisCrawlSpider):
    name = 'news'
    # allowed_domains = ['sina.com.cn']
    # start_urls = ['http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml']
    redis_key = 'sinaspider:start_urls'

    rules = (
        Rule(
            LinkExtractor(
                allow=('index_\d+\.shtml',),  # 允许的链接，正则表达式匹配
                restrict_xpaths=('//div[@class="pagebox"]',),
                # deny=('index_2\.shtml',),  # 不允许的链接，正则表达式
            ),
            callback='parse_item',  # 回调函数
            follow=True,  # 是否跟随
        ),
    )

    def parse_item(self, response):
    # def parse(self, response):
        news_list = response.xpath('//ul[@class="list_009"]/li')
        for news in news_list:
            title = news.xpath('./a/text()').extract_first()
            data_time = news.xpath('./span/text()').extract_first()
            # print(title, data_time)

            item = SinaItem()
            item['title'] = title
            item['data_time'] = data_time
            yield item
# -*- coding: utf-8 -*-
import scrapy
from ..items import QiushiItem

# CrawlSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MyqiushiSpider(CrawlSpider):
    name = 'myqiushi'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    # rules
    rules = [
        Rule(
            LinkExtractor(
                allow=('/text/page/\d+/', '/text/'),
                restrict_xpaths=('//ul[@class="pagination"]',)
            ),
            callback='parse_item',
            follow=True,
        ),
    ]

    #
    def parse_item(self, response):
        print(response.url)
        article_list = response.xpath('//div[@id="content-left"]/div')
        for article in article_list:
            name = article.xpath('./div[contains(@class,"author")]/a[2]/h2/text()').extract_first()
            content = article.xpath('.//div[@class="content"]/span/text()').extract_first().strip()

            item = QiushiItem()
            item['name'] = name
            item['content'] = content
            yield item


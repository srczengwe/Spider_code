# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    title = scrapy.Field()       # 新闻标题
    data_time = scrapy.Field()   # 更新时间
    new_url = scrapy.Field()     # 新闻链接

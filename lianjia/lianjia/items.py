# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class LianjiaItem(scrapy.Item):
    table_name = 'home'
    # name = scrapy.Field()
    title = Field()
    img_url = Field()
    price = Field()
    unitprice = Field()
    li1 = Field()
    li2 = Field()
    li3 = Field()
    li4 = Field()
    li5 = Field()
    li6 = Field()
    li7 = Field()
    li8 = Field()
    li9 = Field()
    li10 = Field()
    li11 = Field()
    li12 = Field()


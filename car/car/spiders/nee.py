# -*- coding: utf-8 -*-
import scrapy


class NeeSpider(scrapy.Spider):
    name = 'nee'
    allowed_domains = ['www.renrenche.com']
    start_urls = ['https://www.renrenche.com/sz/car/ce4d718a6d65601b?plog_id=671958471b3c48e04c092e542f8c138c']

    def parse(self, response):
        print(response.text)
        name = response.xpath('//*[@id="basic"]/div[2]/div[2]/div[1]/div[1]/h1/text()').extract_first()
        print(name)

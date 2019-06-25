# -*- coding: utf-8 -*-
import scrapy
from ..items import LianjiaItem


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['sz.lianjia.com']
    start_urls = ['https://sz.lianjia.com/ershoufang/pg1']

    def parse(self, response):
        home_list = response.xpath('//div[@class="leftContent"]/ul/li')
        for home in home_list:
            item = LianjiaItem()
            # 房屋标题
            title = home.xpath('./div[@class="info clear"]/div[@class="title"]/a/text()').extract_first()
            if title != None:
                item['title'] = title

            # 详情链接
            detail_url = home.xpath('./div[@class="info clear"]/div[@class="title"]/a/@href').extract_first()
            if detail_url != None:
                requset = scrapy.Request(url=detail_url, callback=self.get_detail)
                requset.meta['item'] = item
                yield requset

        url = 'https://sz.lianjia.com/ershoufang/pg%d'
        for num in range(1, 101):
            page_url = url % num
            yield scrapy.Request(url=page_url, callback=self.parse)

    # 房屋详情
    def get_detail(self, response):
        item = response.meta['item']
        # 缩略图
        item['img_url'] = response.xpath('//div[@class="imgContainer"]/img/@src').extract_first()
        # 总价格
        item['price'] = response.xpath('//div[@class="content"]/div[@class="price "]/span[@class="total"]/text()').extract_first()
        # 每平米的价格
        item['unitprice'] = response.xpath('//div[@class="content"]/div[@class="price "]/div[@class="text"]/div/span/text()').extract_first()
        # 小区名
        labe = response.xpath('//div[5]/div[2]/div[4]/div[1]/a[1]/text()').extract_first()
        # 是否预约
        visittime = response.xpath('//div[5]/div[2]/div[4]/div[3]/span[2]/text()').extract_first()
        # 基本属性
        content_list = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul')
        for content in content_list:
            item['li1'] = content.xpath('./li[1]/text()').extract_first()     # 房屋户型
            item['li2'] = content.xpath('./li[2]/text()').extract_first()     # 所在楼层
            item['li3'] = content.xpath('./li[3]/text()').extract_first()     # 建筑面积
            item['li4'] = content.xpath('./li[4]/text()').extract_first()     # 户型结构
            item['li5'] = content.xpath('./li[5]/text()').extract_first()     # 套内面积
            item['li6'] = content.xpath('./li[6]/text()').extract_first()     # 建筑类型
            item['li7'] = content.xpath('./li[7]/text()').extract_first()     # 房屋朝向
            item['li8'] = content.xpath('./li[8]/text()').extract_first()     # 建筑结构
            item['li9'] = content.xpath('./li[9]/text()').extract_first()     # 装修情况
            item['li10'] = content.xpath('./li[10]/text()').extract_first()     # 梯户比例
            item['li11'] = content.xpath('./li[11]/text()').extract_first()     # 配备电梯
            item['li12'] = content.xpath('./li[12]/text()').extract_first()     # 产权年限
            yield item










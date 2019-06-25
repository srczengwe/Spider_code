# -*- coding: utf-8 -*-
import scrapy
from ..items import BiqugeItem


class XuanhuanSpider(scrapy.Spider):
    name = 'xuanhuan'
    allowed_domains = ['biquge5200.cc']
    start_urls = ['https://www.biquge5200.cc/xuanhuanxiaoshuo/']

    # 小说列表
    def parse(self, response):
        # print(response.text)

        xs_list = response.xpath('//*[@id="newscontent"]/div[1]/ul/li')
        # print(len(xs_list))

        for xs in xs_list:
            name = xs.xpath('./span[@class="s2"]/a/text()').extract_first()
            href = xs.xpath('./span[@class="s2"]/a/@href').extract_first()
            # print(href)

            # 请求 获取小说的章节
            yield scrapy.Request(url=href,
                                 callback=self.get_section,
                                 meta={'name': name}
                        )

    # 章节
    def get_section(self, response):
        name = response.meta.get('name')
        zj_list = response.xpath('//div[@id="list"]/dl/dd')
        # print(len(zj_list))
        for zj in zj_list:
            section = zj.xpath('./a/text()').extract_first()
            href = zj.xpath('./a/@href').extract_first()
            # print(href)
            # 请求 每个章节的内容
            yield scrapy.Request(url=href,
                                 callback=self.get_content,
                                 meta={'name': name, 'section': section}
                        )

    # 内容
    def get_content(self, response):
        # print("response")
        name = response.meta.get('name')
        section = response.meta.get('section')
        content = "\n".join(response.xpath('//div[@id="content"]/p/text()').extract())
        # print(content)

        item = BiqugeItem()
        item['name'] = name
        item['section'] = section
        item['content'] = content
        yield item





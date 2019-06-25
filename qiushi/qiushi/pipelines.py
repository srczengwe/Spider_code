# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QiushiPipeline(object):

    def open_spider(self, spider):
        self.fp = open('qiushi.txt', 'a', encoding='utf-8')

    # 会被调用很多次
    def process_item(self, item, spider):

        string = str((item['name'], item['content'])) + "\n"
        self.fp.write(string)
        self.fp.flush()

        return item

    def close_spider(self, spider):
        self.fp.close()

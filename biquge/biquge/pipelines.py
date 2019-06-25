# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class BiqugePipeline(object):

    def __init__(self):
        self.path = r"I:\python_spider\biquge"

    def process_item(self, item, spider):
        name = item['name']
        section = item['section']
        content = item['content']

        # 判断小说文件夹是否存在, 如果不存在则创建
        xs_path = os.path.join(self.path, name)
        if not os.path.exists(xs_path):
            os.mkdir(xs_path)

        # 给章节文件写入内容
        file_path = os.path.join(xs_path, section+".txt")
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(content)
            fp.flush()

        print(name, section, "存储成功！")

        return item

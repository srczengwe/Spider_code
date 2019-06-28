# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class SinaPipeline(object):
    # 将数据存入本地
    # def __init__(self):
    #     pass
    #
    # def open_spider(self,spider):
    #     print('开始爬取......')
    #     self.fp = open('news.txt', 'a', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     string = str((item['title'], item['data_time'])) + '\n'
    #     self.fp.write(string)
    #     self.fp.flush()
    #     return item
    #
    # def close_spider(self,spider):
    #     print('爬取结束......')
    #     self.fp.close()

    # 将数据存入数据库
    def __init__(self):
        pass

    def open_spider(self, spider):
        # print('开始爬取......')
        # 连接mysql数据库
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='root',
                                  database='sina',
                                  charset='utf8')
        # 创建游标
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # 获取item中的数据
        title = item.get('title')
        data_time = item.get('data_time')
        new_url = item.get('new_url')

        # 书写sql语句
        sql = 'insert into news(title, data_time, new_url) values("%s","%s", "%s")' % (title, data_time, new_url)
        self.cursor.execute(sql)
        self.db.commit()
        return item

    def close_spider(self, spider):
        # print('爬取结束......')
        self.cursor.close()
        self.db.close()

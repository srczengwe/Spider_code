# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class XpcPipeline(object):

    # 打开爬虫
    def open_spider(self, spider):
        self.db = pymysql.connect(host='127.0.0.1',
                                  port=3306,
                                  user='root',
                                  password='root',
                                  database='xpc_1810',
                                  charset='utf8mb4')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        keys, values = zip(*item.items())

        # sql
        sql = 'insert into `{}`({}) values({}) on duplicate key update {}'.format(
            item.table_name,  # 表名
            ','.join(['`%s`'%key for key in keys]),  # 所有字段
            ','.join(['%s']*len(keys)),  # 多个%s
            ','.join(['`{}`=%s'.format(key) for key in keys])
        )
        # 执行sql
        self.cursor.execute(sql, values*2)
        self.db.commit()

        print('ok')

        return item

    # 关闭爬虫
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()







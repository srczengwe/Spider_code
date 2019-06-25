# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        if item.table_name == 'home':
            db = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                                 password="root", database="lianjia", charset="utf8")

            # 获取游标
            cursor = db.cursor()
            # 指定数据表
            table = 'home'

            # 要插入数据库的数据
            item = {
                'title': item['title'],
                'img_url': item['img_url'],
                'price': item['price'],
                'unitprice': item['unitprice'],
                'li1': item['li1'],
                'li2': item['li2'],
                'li3': item['li3'],
                'li4': item['li4'],
                'li5': item['li5'],
                'li6': item['li6'],
                'li7': item['li7'],
                'li8': item['li8'],
                'li9': item['li9'],
                'li10': item['li10'],
                'li11': item['li11'],
                'li12': item['li12'],

            }

            # 往表中插入数据
            keys = ",".join(item.keys())
            values = ",".join(["%s"] * len(item))
            sql = f"insert into {table}({keys}) values({values})"

            try:
                cursor.execute(sql, (tuple(item.values())))
                print("数据存储成功!")
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                print("数据存储失败!")

            return item


import pymysql
from redis import Redis
import json
# 从redis中取数据,然后存到mysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root',
                       charset='utf8', database='sina')

cursor = conn.cursor()
redis_conn = Redis()


def main():
    while True:
        # 从redis中取数据
        try:
            _, data = redis_conn.brpop('news:items', timeout=60)
        except Exception:
            cursor.close()
            conn.close()
            break
        # 转化为python对象
        data = json.loads(data, encoding='utf-8')
        print(data)

        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f'insert into top({keys}) values({values})'

        try:
            cursor.execute(sql, (tuple(data.values())))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


if __name__ == '__main__':
    main()

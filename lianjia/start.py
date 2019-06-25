import scrapy.cmdline


# 执行scrapy命令
def main():
    # 启动项目并打印日志
    # scrapy.cmdline.execute(['csrapy', 'crawl', 'homelink'])   # 启动项目方式一
    scrapy.cmdline.execute('scrapy crawl homelink'.split())   # 启动项目方式二
    # scrapy.cmdline.execute('scrapy crawl home'.split())   # 启动项目方式二

    # 启动项目不打印日志
    # scrapy.cmdline.execute('scrapy crawl home --nolog'.split())   # 启动项目方式三

    # 执行命令保存成json文件
    # scrapy.cmdline.execute('scrapy crawl homelink -o book.json --nolog'.split())
    # 执行命令保存成xml文件
    # scrapy.cmdline.execute('scrapy crawl homelink -o book.xml --nolog'.split())
    # 执行命令保存成csv文件
    # scrapy.cmdline.execute('scrapy crawl homelink -o book.csv --nolog'.split())


# 项目主入口
if __name__ == '__main__':
    main()
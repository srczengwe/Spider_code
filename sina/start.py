import scrapy.cmdline


# 执行scrapy命令
def main():
    # 启动爬虫显示日志
    # scrapy.cmdline.execute(['scrapy', 'crawl', 'news'])
    scrapy.cmdline.execute("scrapy crawl news".split())
    # 启动爬虫,但不显示日志
    # scrapy.cmdline.execute("scrapy crawl news --nolog".split())
    # 通过命令保存成json文件
    # scrapy.cmdline.execute("scrapy crawl news -o news.json --nolog".split())
    # 通过命令保存成xml文件
    # scrapy.cmdline.execute("scrapy crawl news -o news.xml --nolog".split())
    # 通过命令保存成csv文件
    # scrapy.cmdline.execute("scrapy crawl news -o news.csv --nolog".split())


if __name__ == '__main__':
    main()

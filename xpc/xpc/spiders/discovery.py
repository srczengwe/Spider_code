# -*- coding: utf-8 -*-
import json
import re

import scrapy
from ..items import *


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']

    # 产品列表
    def parse(self, response):
        li_list = response.xpath('//ul[@class="video-list"]/li')
        for li in li_list:
            # 作品id
            pid = li.xpath('./@data-articleid').extract_first()
            # 标题
            title = li.xpath('.//div[@class="video-con-top"]/a/p/text()').get()
            # 缩略图
            thumbnail = li.xpath('./a/img/@_src').extract_first()
            # 作品分类
            category_list = li.xpath('.//div[@class="new-cate"]/span[@class="fs_12 fw_300 c_b_9"]/text()').extract()
            category = '|'.join([c.strip() for c in category_list])
            # 发布时间
            created_at = li.xpath('.//div[@class="video-hover-con"]/p/text()').get()
            # 点赞次数
            like_counts = li.xpath('.//span[@class="fw_300 c_b_9 icon-like"]/text()').get()
            # 作品描述
            description = li.xpath('.//div[@class="video-hover-con"]/div/text()').get()
            # 作品详情url
            post_url = 'http://www.xinpianchang.com/a%s?from=ArticleList' % pid

            # item
            item = PostItem()
            item['pid'] = pid
            item['title'] = title
            item['thumbnail'] = thumbnail
            item['category'] = category
            item['created_at'] = created_at
            item['like_counts'] = like_counts
            item['description'] = description

            # 请求产品详情页
            request = scrapy.Request(url=post_url, callback=self.get_post)
            request.meta['item'] = item
            yield request

    # 产品post详情
    def get_post(self, response):
        item = response.meta.get('item')
        pid = item.get('pid')
        # 播放次数
        item["play_counts"] = response.xpath('//i[@class="fs_12 fw_300 c_b_6 v-center play-counts"]/@data-curplaycounts').get()
        # 视频数据
        vid, = re.findall('vid: \"(.*?)\"', response.text)
        video_url = "https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource,resource_origin?" % vid
        # 获取视频数据
        request = scrapy.Request(url=video_url, callback=self.get_video)
        request.meta['item'] = item
        yield request

        # 创建者
        li_list = response.xpath('//div[@class="filmplay-creator right-section"]/ul/li')
        for li in li_list:
            cid = li.xpath('./a/@data-userid').get()
            href = "http://www.xinpianchang.com" + li.xpath('./a/@href').get()

            composer_item = ComposerItem()
            composer_item['cid'] = cid

            request2 = scrapy.Request(url=href, callback=self.get_composer)
            request2.meta['item'] = composer_item
            yield request2

            # copyright
            cr_item = CopyringhtItem()
            cr_item['pcid'] = "%s_%s" % (pid, cid)
            cr_item['pid'] = pid
            cr_item['cid'] = cid
            cr_item['roles'] = li.xpath('.//*[contains(@class, "roles")]/text()').get()
            yield cr_item

        # 评论
        comment_url = "http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&ajax=0&page=1" % pid
        request3 = scrapy.Request(comment_url, callback=self.get_comment)
        yield request3

    # 获取视频数据
    def get_video(self, response):
        item = response.meta.get('item')
        # 对视频数据进行json解析
        content = json.loads(response.text)
        # 视频预览图
        item['preview'] = content['data']['video']['cover']
        # 视频链接
        item['video'] = content['data']['resource']['default']['url']
        # 视频格式
        item['video_format'] = content['data']['resource']['default']['video_codec_name']
        # 播放时长
        item['duration'] = content['data']['resource']['default']['duration']

        yield item

    # 获取创作者数据
    def get_composer(self, response):
        item = response.meta.get('item')
        # banner
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        banner = re.findall('background\-image:url\((.*?)\)', banner)[0]
        item['banner'] = banner
        # 头像
        item['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        # 是否加V
        verified = response.xpath('//span[@class="avator-wrap-s"]/span[contains(@class, "author-v")]').get()
        item['verified'] = 'yes' if verified else 'no'
        # 名字
        item['name'] = response.xpath('//*[@class="creator-info"]//*[contains(@class,"creator-name")]/text()').get()
        # 自我介绍
        item['intro'] = response.xpath('//*[@class="creator-info"]//*[contains(@class,"creator-desc")]/text()').get()
        # 被点赞次数
        like_counts = response.xpath('//*[@class="creator-info"]//*[contains(@class,"creator-detail")]/span[1]/span[2]/text()').get()
        item['like_counts'] = like_counts.replace(',', "")
        # 粉丝数量
        item['fans_counts'] = response.xpath(
            '//*[@class="creator-info"]//*[contains(@class,"creator-detail")]/span[2]/span[2]/@data-counts').get()
        # 关注数量
        item['follow_counts'] = response.xpath(
            '//*[@class="creator-info"]//*[contains(@class,"creator-detail")]/span[3]/span[2]/text()').get()
        # 所在位置
        item['location'] = response.xpath(
            '//*[@class="creator-info"]//*[contains(@class,"creator-detail")]/span[5]/text()').get()
        # 职业
        career = response.xpath(
            '//*[@class="creator-info"]//*[contains(@class,"creator-detail")]/span[7]/text()').get()
        career = career if career else '-'
        item['career'] = career

        yield item

    # 获取评论
    def get_comment(self, response):
        content = json.loads(response.text)
        comment_list = content.get('data').get('list')
        for comment in comment_list:
            item = CommentItem()
            item['commentid'] = comment['commentid']
            item['pid'] = comment['articleid']
            item['cid'] = comment['userInfo']['userid']
            item['avatar'] = comment['userInfo']['face']
            item['uname'] = comment['userInfo']['username']
            item['created_at'] = comment['addtime_int']
            item['content'] = comment['content']
            item['like_counts'] = comment['count_approve']
            item['reply'] = comment['commentid']

            yield item

        # 下一页
        next_page_url = content.get('data').get('next_page_url')
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.get_comment)





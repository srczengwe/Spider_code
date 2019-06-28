# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# 作品Item
class PostItem(Item):
    # 表名
    table_name = 'posts'

    pid = Field()  # 作品id
    title = Field()  # 作品title
    thumbnail = Field()  # 视频缩略图
    preview = Field()  # 视频预览图
    video = Field()  # 视频链接
    video_format = Field()  # 视频格式：等
    category = Field()  # 作品分类
    duration = Field()  # 播放时长
    created_at = Field()  # 发表时间
    play_counts = Field()  # 播放次数
    like_counts = Field()  # 被点赞次数
    description = Field()  # 作品描述


# 创作者Item
class ComposerItem(Item):
    # 表名
    table_name = 'composers'

    cid = Field()  # 创作者id
    banner = Field()  # 用户主页banner图片
    avatar = Field()  # 用户头像
    verified = Field()  # 是否加V
    name = Field()  # 名字
    intro = Field()  # 自我介绍
    like_counts = Field()  # 被点赞次数
    fans_counts = Field()  # 粉丝数量
    follow_counts = Field()  # 关注数量
    location = Field()  # 所在位置
    career = Field()  # 职业


# 评论
class CommentItem(Item):
    # 表名
    table_name = 'comments'

    commentid = Field()  # 评论表主键
    pid = Field()  # 评论表主键
    cid = Field()  # 评论人ID
    avatar = Field()  # 评论人头像
    uname = Field()  # 评论人名称
    created_at = Field()  # 发表时间
    content = Field()  # 评论内容
    like_counts = Field()  # 被点赞次数
    reply = Field()  # 回复其他评论的ID，如果不是则为0


# copyright
class CopyringhtItem(Item):
    # 表名
    table_name = 'copyrights'

    pcid = Field()  # 主键，由pid_cid组成
    pid = Field()  # 对应作品表主键
    cid = Field()  # 对应作者表主键
    roles = Field()  # 担任角色






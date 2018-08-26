# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FudanbbsspiderItem(scrapy.Item):
    
    board_cate = scrapy.Field() #板块种类
    board_url = scrapy.Field() #板块url链接 
    board_name_cn = scrapy.Field() #板块中文名称
    board_name_en = scrapy.Field() #板块英文名称
    
    thread_page_url = scrapy.Field() #帖子组所在页面
    thread_title = scrapy.Field()
    
    post_url = scrapy.Field() #post_card的url
    post_id = scrapy.Field() #发帖人ID
    post_time = scrapy.Field() #发帖时间
    
    reply_id = scrapy.Field() #回复对象ID
    content = scrapy.Field() #发帖内容
    

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class FudanbbsspiderPipeline(object):
    def __init__(self):
        f = open("/Users/hnyang/fudanbbsData/data.csv",'x',encoding='utf-8') #新创建一个文件
        writer = csv.writer(f)
        writer.writerow(('post_time','post_id',"reply_id",'content','post_url','thread_title','thread_page_url','board_cate','board_name_cn','board_name_en','board_url'))
        

    def process_item(self, item, spider):
        
        f = open('/Users/hnyang/fudanbbsData/data.csv','a+',encoding = 'utf-8') 
        writer = csv.writer(f)
        writer.writerow((item['post_time'],item['post_id'],item["reply_id"],item['content'],item['post_url'],item['thread_title'],item['thread_page_url'],item['board_cate'],item['board_name_cn'],item['board_name_en'],item['board_url']))
        return item

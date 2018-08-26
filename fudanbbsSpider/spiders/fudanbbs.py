# -*- coding: utf-8 -*-
import scrapy
from fudanbbsSpider.items import FudanbbsspiderItem
from scrapy.loader.processors import Join, MapCompose
from scrapy.selector import Selector
from scrapy.http import Request

class FudanbbsSpider(scrapy.Spider):
    name = 'fudanbbs'
    allowed_domains = ['bbs.fudan.edu.cn']
    start_urls = ['https://bbs.fudan.edu.cn/bbs/boa?s=1']

    def parse(self, response):
        
        items_1 = []
        
        selector = Selector(response)
        boards = selector.xpath('//brd')
        
        for board in boards:
            
            item = FudanbbsspiderItem()
            
            board_name_en = board.xpath('@title').extract()[0]
            item['board_name_en'] = board_name_en
            item['board_cate'] = board.xpath('@cate').extract()[0]
            item['board_url'] = 'https://bbs.fudan.edu.cn/bbs/doc?board=' + board_name_en
            item['board_name_cn'] = board.xpath('@desc').extract()[0]
            
            
            self.log(item['board_name_en'])
            self.log(item['board_cate'])
            self.log(item['board_url'])
            self.log(item['board_name_cn'])
            
            items_1.append(item)
            
        for item in items_1:
            yield Request(url=item['board_url'], meta={'item_1': item}, callback=self.parse2)
                
        
    def parse2(self, response): #获取板块的所有页面（讨论区翻页）
            
        item_1 = response.meta['item_1']  
            
        items = []
            
        bid = response.xpath('//brd/@bid').extract()[0]
        total = int(response.xpath('//brd/@total').extract()[0])
            
            
        for page in range(1, total//20 + 2):
                
            item = FudanbbsspiderItem()
            start = 20 * page - 19
                
            thread_page_url = 'https://bbs.fudan.edu.cn/bbs/doc?bid='+bid+'&start='+str(start)
            
            item['board_cate'] = item_1['board_cate'] 
            item['board_url'] = item_1['board_url'] 
            item['board_name_en'] = item_1['board_name_en'] 
            item['board_name_cn'] = item_1['board_name_cn']                        
            item['thread_page_url'] = thread_page_url
            #self.log(item['thread_page_url'])   
            items.append(item)
                
            for item in items:
                yield Request(url=item['thread_page_url'], meta={'item_2':item},callback=self.parse3)
        
    def parse3(self, response):
            
        item_2 = response.meta['item_2']
        items =[]
            
        selector = Selector(response)
        bid = response.xpath('//brd/@bid').extract()[0]
        threads = selector.xpath('//po[@nore="1" and @m="N"]')
        
        for thread in threads:
            item = FudanbbsspiderItem()
            item['board_cate'] = item_2['board_cate']
            item['board_url'] = item_2['board_url']
            item['board_name_en'] = item_2['board_name_en']
            item['board_name_cn'] = item_2['board_name_cn']
            item['thread_page_url'] = item_2['thread_page_url']
            
            item['post_id'] = thread.xpath('@owner').extract()[0]
            post_time_r = thread.xpath('@time').extract()[0]
            item['post_time'] = MapCompose(lambda i: i.replace('T',' '),str)(post_time_r)[0]
            item['post_url'] = 'https://bbs.fudan.edu.cn/bbs/con?new=1&bid='+bid+'&f='+thread.xpath('@id').extract()[0]
            
            item['thread_title'] = thread.xpath('text()').extract()[0]
            
            self.log(item['thread_title'])
            self.log(item['post_url'])
        
            items.append(item)
        
        for item in items:
            yield Request(url=item['post_url'], meta={'item_3':item},callback=self.parse4)
    
    
    def parse4(self, response):
        
        item_3 = response.meta['item_3']
        
        item = FudanbbsspiderItem()
        item['board_cate'] = item_3['board_cate']
        item['board_url'] = item_3['board_url']
        item['board_name_en'] = item_3['board_name_en']
        item['board_name_cn'] = item_3['board_name_cn']
        item['thread_page_url'] = item_3['thread_page_url']
        
        item['post_id'] = item_3['post_id']
        item['post_time'] = item_3['post_time']
        item['post_url'] = item_3['post_url']
            
        item['thread_title'] = item_3['thread_title']
        
        item['content'] = Join()(response.xpath('//pa[@m="t"]/p/text()').extract())
        
        if len(response.xpath('//pa[@m="q"]/p/text()'))==0:
            item['reply_id']=''
        else:             
            if len(response.xpath('//pa[@m="q"]/p[1]/text()').re('\xa0在\xa0(.*)\xa0\('))==0:
                item['reply_id'] = response.xpath('//pa[@m="q"]/p[1]/text()').re('\xa0在\xa0(.*)\xa0的大作')[0]
            else:
                item['reply_id'] = response.xpath('//pa[@m="q"]/p[1]/text()').re('\xa0在\xa0(.*)\xa0\(')[0]
                
        self.log(item['board_cate'])
        self.log(item['board_url'])
        self.log(item['board_name_en'])
        self.log(item['board_name_cn'])
        self.log(item['thread_page_url'])
        self.log(item['post_id'])
        self.log(item['post_time'])
        self.log(item['post_url'])
            
        self.log(item['thread_title'])
        
        self.log(item['content'])
        self.log(item['reply_id'])
        
        
        return item
        
            
            
                
            
            
            
            
            
            
            
            
            
            
            
            
            

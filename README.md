# fudanbbsSpider
复旦大学官方校园bbs（日月光华：https://bbs.fudan.edu.cn ）论坛爬虫

## 爬取以下内容：

    board_cate  #板块种类
    board_url  #板块url链接 
    board_name_cn #板块中文名称
    board_name_en #板块英文名称
    
    thread_page_url  #帖子组所在页面url（由start决定）
    thread_title = #帖子标题
    
    post_url = scrapy.Field() #post_card的url
    post_id = scrapy.Field() #发帖人ID
    post_time = scrapy.Field() #发帖时间
    
    reply_id = scrapy.Field() #回复对象ID
    content = scrapy.Field() #发帖内容

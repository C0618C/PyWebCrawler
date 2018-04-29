import scrapy
import re
import _setting_

# scrapy runspider anime.py -o o/idx.json

class AnimeSpider(scrapy.Spider):
    name = 'animespider'
    start_urls = _setting_.target_url  #['https://blog.scrapinghub.com']
    allowed_domains =[re.search('//([^/]*)/+',start_urls[0]).group(1)]
    _scheme = re.search('^https?:',start_urls[0]).group()

    custom_settings = {
        'LOG_FILE':'o/scrapy.log'
    }

    def parse(self, response):
        for tt in response.selector.css('.k_list-lb'):  # 列表规则
            '''   只爬取目录信息
            item = {}
            item['title'] = tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/text()').extract()[0] # 标题
            item['url'] = tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/@href').extract()[0] # 目标地址
            item['img'] = tt.xpath('.//*[@class="lz_img"]/img/@src').extract()[0]  #封面地址
            item['date']=tt.css('#k_list-lb-2-f::text').extract()[0][3:]  # 更新时间
            yield item
            '''

            next_url=self._scheme+"//"+self.allowed_domains[0]+tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/@href').extract()[0]
            self.log('Going to next page:\t '+next_url)
            yield scrapy.Request(next_url, callback=self.parse_page)
        
        # 翻页
        __next=response.selector.css('.k_pape').xpath('a[text()="下一页"]/@href').extract()
        if _setting_.isDeep and len(__next)>0:
            next_url = self._scheme+"//"+self.allowed_domains[0]+__next[0]
            self.log('Going to next page:\t '+next_url)
            yield scrapy.Request(next_url, callback=self.parse)


    # 爬取每一页
    def parse_page(self, response):
        anime_page = {}
        anime_page['title']=response.css('.k_jianjie-3a-1-name::text').extract()[0]
        anime_page['preview']=response.xpath('//*[@id="k_jianjie-2b"]/a/img/@src').extract()[0]
        anime_page['date']=response.xpath('//*[@class="k_jianjie-3a-2b"]/text()').extract()[2]
        anime_page['url']=response.url[len(self._scheme+"//"+self.allowed_domains[0]):]
        anime_page['down']=response.css('.k_jianjie-3a-5down::text').extract()[0].replace(" ",'').replace("\r\n",'')
        anime_page['img']=response.xpath('//*[@class="content"]/p/img/@src').extract()
        yield anime_page

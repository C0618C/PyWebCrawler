import scrapy
import _tgURL

class AnimeSpider(scrapy.Spider):
    name = 'animespider'
    start_urls = _tgURL.target_url  #target_url= ['https://blog.scrapinghub.com']

    def parse(self, response):
        for tt in response.selector.css('.k_list-lb'):  # 列表规则
            item = {}
            item['title'] = tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/text()').extract()[0] # 标题
            item['url'] = tt.xpath('.//*[@class="k_list-lb-2"]/div[1]/a/@href').extract()[0] # 目标地址
            item['img'] = tt.xpath('.//*[@class="lz_img"]/img/@src').extract()[0]  #封面地址
            item['date']=tt.css('#k_list-lb-2-f::text').extract()[0][3:]  # 更新时间
            yield item
        
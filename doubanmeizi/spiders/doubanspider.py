from doubanmeizi.items import DoubanmeiziItem

__author__ = 'tropsci'

import scrapy

class DoubanSpider(scrapy.spiders.Spider):
    name = "douban"
    allowed_domains = ["doubanmeizi.com"]
    start_urls = [
        "http://www.doubanmeizi.com/"
    ]

    def parse(self, response):
        for detail_path in response.xpath("//a[@target='_blank']/@href"):
            yield scrapy.Request(response.urljoin(detail_path.extract()), callback=self.parse_page)

        next_urls = response.xpath("//a[@class='nextpostslink']/@href").extract()
        for next_url in next_urls:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

    def parse_page(self, response):
        for image in response.xpath("//div[@id='picture']/p/img"):
            item = DoubanmeiziItem()
            item["desc"] = image.xpath("@alt").extract()[0]
            item["link"] = image.xpath("@src").extract()
            item["title"] = image.xpath("@alt").extract()[0]
            item["image_urls"] = image.xpath("@src").extract()
            item["images"] = image.xpath("@src").extract()
            return item

from doubanmeizi.items import DoubanmeiziItem

__author__ = 'tropsci'

import scrapy

class DoubanSpider(scrapy.spiders.Spider):
    name = "douban"
    allowed_domains = ["doubanmeinv.com"]
    start_urls = [
        "http://doubanmeinv.com/"
    ]

    def parse(self, response):
        for detail_path in response.xpath("//a[@target='_topic_detail']/@href"):
            yield scrapy.Request(response.urljoin(detail_path.extract()), callback=self.parse_page)

        next_urls = response.xpath("//li[@class='next next_page']/a/@href").extract()
        if len(next_urls) > 0:
            for next_url in next_urls:
                yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        else:
            next_urls = response.xpath("//ul[@class='pagination']/li")
            next_page = ""
            for next_url in next_urls:
                if self.isCurrentPage(next_url.xpath("@class='thisclass'").extract()):
                    next_page = "placeholder"
                    continue
                if next_page == "placeholder":
                    next_page = next_url.xpath("a/@href").extract()[0]
                    yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_page(self, response):
        for image in response.xpath("//div[@class='topic-figure cc']/img"):
            item = DoubanmeiziItem()
            item["desc"] = image.xpath("@alt").extract()[0]
            item["link"] = image.xpath("@src").extract()
            item["title"] = image.xpath("@alt").extract()
            item["image_urls"] = image.xpath("@src").extract()
            item["images"] = image.xpath("@src").extract()
            print item
            return item


    def isCurrentPage(self, paths):
        isCurrent = False
        for path in paths:
            isCurrent = path == u'1'
            break
        return isCurrent
from doubanmeizi.items import DoubanmeiziItem

__author__ = 'tropsci'

import scrapy
from  urlparse import urlparse

class DoubanSpider(scrapy.spiders.Spider):
    name = "douban"
    start_urls = [
        "http://www.doubanmeizi.com/"
    ]

    def parse(self, response):
        categories = []

        for category_xpath in response.xpath("//div[@class='nav']/ul/li/a/@href"):
            category_path = category_xpath.extract()
            url_path = urlparse(category_path)[2]
            category_name = url_path.split("/")[-2]
            categories.append((category_name, category_path))

            yield scrapy.Request(category_path, meta={'category': category_name}, callback=self.parse_category)


    def parse_category(self, response):
        for detail_path in response.xpath("//a[@target='_blank']/@href"):
            yield scrapy.Request(response.urljoin(detail_path.extract()), meta=response.meta, callback=self.parse_page)

        next_urls = response.xpath("//a[@class='nextpostslink']/@href").extract()
        for next_url in next_urls:
            yield scrapy.Request(response.urljoin(next_url), meta=response.meta, callback=self.parse_category)


    def parse_page(self, response):
        category = response.meta['category']
        image_number = 0
        for image in response.xpath("//div[@id='picture']/p/img"):
            item = DoubanmeiziItem()

            item["desc"] = image.xpath("@alt").extract()[image_number]
            item["link"] = image.xpath("@src").extract()
            item["title"] = image.xpath("@alt").extract()[image_number]
            item["image_urls"] = image.xpath("@src").extract()
            item["images"] = image.xpath("@src").extract()
            item["category"] = category
            item["width"] = image.xpath("@width").extract()[image_number]
            item["height"] = image.xpath("@height").extract()[image_number]
            image_number += 1
            print(item)

            yield item

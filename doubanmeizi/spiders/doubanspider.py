from doubanmeizi.items import DoubanmeiziItem

__author__ = 'tropsci'

import scrapy
from  urlparse import urlparse

class DoubanSpider(scrapy.spiders.Spider):
    name = "douban"
    allowed_domains = ["doubanmeizi.com"]
    start_urls = [
        "http://www.doubanmeizi.com/"
    ]

    __category = "all"
    __category_number = 0

    def parse(self, response):

        categories = []
        for category_xpath in response.xpath("//div[@class='nav']/ul/li/a/@href"):
            category_path = category_xpath.extract()
            url_path = urlparse(category_path)[2]
            category_name = url_path.split("/")[-2]
            categories.append((category_name, category_path))

            print("*****************" + category_name)
            yield scrapy.Request(category_path, callback=self.parse_category)

        # print(categories)
        #
        # category = categories[self.__category_number]
        # self.__category = category[0]
        # category_path = category[1]
        # if self.__category_number < len(categories):
        #     print("++++++++++++++++" + self.__category)
        #     self.__category_number += 1
        #     yield scrapy.Request(category_path, callback=self.parse_category)
        #
        #     print("---------------" + self.__category)
        #
        #     yield scrapy.Request("http://www.doubanmeizi.com/", callback=self.parse)


    def parse_category(self, response):
        for detail_path in response.xpath("//a[@target='_blank']/@href"):
            yield scrapy.Request(response.urljoin(detail_path.extract()), callback=self.parse_page)

        next_urls = response.xpath("//a[@class='nextpostslink']/@href").extract()
        for next_url in next_urls:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse_category)


    def parse_page(self, response):
        for image in response.xpath("//div[@id='picture']/p/img"):
            item = DoubanmeiziItem()
            item["desc"] = image.xpath("@alt").extract()[0]
            item["link"] = image.xpath("@src").extract()
            item["title"] = image.xpath("@alt").extract()[0]
            item["image_urls"] = image.xpath("@src").extract()
            item["images"] = image.xpath("@src").extract()
            item["category"] = self.__category
            print "_____________"
            print(item)
            return item

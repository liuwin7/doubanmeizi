# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

from ImageDatabaseItem import ImageDatabaseItem
from DBManager import DBManager

class DoubanmeiziPipeline(ImagesPipeline):

    dbManager = DBManager("/Users/tropsci/Desktop/doubanImages/doubanmeizi.db")

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        image_name = item["title"]
        image_category_name = item['category']
        image_width = item["width"]
        image_height = item["height"]

        image_items = [x for ok, x in results if ok]
        for image_path_item in image_items:
            print("__________")
            print(image_path_item)
            image_url = image_path_item["url"]
            image_path = image_path_item["path"]
            image_checksum = image_path_item["checksum"]

            imageDatabaseItem = ImageDatabaseItem(image_name, image_url, image_path, image_checksum, image_category_name, image_width, image_height)
            self.dbManager.insertDatabaseImageItem(imageDatabaseItem)

        return item
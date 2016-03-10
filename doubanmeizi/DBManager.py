__author__ = 'tropsci'

import os
import sqlite3

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from scrapy import log
from ImageDatabaseItem import ImageDatabaseItem

class DBManager:

    def __init__(self, database_path):
        self.database_path = database_path
        if (not os.path.isabs(database_path)):
            self.database_path = os.getcwd().join(database_path)

        conn = sqlite3.connect(self.database_path)
            # image table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ImageTable
            (image_id INTEGER primary key,
            image_name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            image_path TEXT NOT NULL,
            image_checksum TEXT NOT NULL,
            image_category_name TEXT NOT NULL
            );
            ''')
        conn.commit()
        conn.close()


    def insertDatabaseImageItem(self, databaseImageItem):
        conn = sqlite3.connect(self.database_path)
        sql = '''
        INSERT INTO ImageTable(image_id, image_name, image_url, image_path, image_checksum, image_category_name)
        VALUES (
                NULL, '{image_name}', '{image_url}', '{image_path}', '{image_checksum}', '{image_category_name}'
        );
        '''.format(
                   image_name = databaseImageItem.image_name,
                   image_url = databaseImageItem.image_url,
                   image_path = databaseImageItem.image_path,
                   image_checksum = databaseImageItem.image_checksum,
                   image_category_name = databaseImageItem.image_category_name)
        scrapy.log.msg(sql, level=scrapy.log.DEBUG)
        conn.execute(sql)
        conn.commit()
        conn.close()

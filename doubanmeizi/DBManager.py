__author__ = 'tropsci'

import os
import sqlite3

from ImageDatabaseItem import ImageDatabaseItem

class DBManager:

    __database_path = ":memory:"

    def __init__(self, database_path):
        __database_path = database_path
        if (not os.path.isabs(database_path)):
            __database_path = os.getcwd().join(database_path)
        if (not os.path.exists(__database_path)):  # if database file not exist , init database file
            conn = sqlite3.connect(__database_path)
            # image table
            # image_category 1:清新  3:美腿 4:美臀 45:gif 5:美胸
            conn.execute('''
            CREATE TABLE IF NOT EXISTS ImageCategory
            (
            category_id INT PRIMARY KEY NOT NULL,
            category_name TEXT NOT NULL,
            )
            ''')
            conn.execute('''
            CREATE TABLE IF NOT EXISTS image
            (image_id INT PRIMARY KEY NOT NULL,
            image_name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            image_path TEXT NOT NULL,
            image_thumb_path TEXT,
            image_checksum TEXT NOT NULL,
            image_category_id INT NOT NULL,
            FOREIGN KEY(image_category) REFERENCES ImageCategory(category_id)
            );
            ''')
            category_dic = {
                "1":"清新",
                "3":"美腿",
                "4":"美臀",
                "45":"gif",
                "5":"美胸"
            }
            # init category table
            for category_id in category_dic:
                category_name = category_dic[category_id]
                conn.execute('''
                INSERT INTO ImageCategory(category_id, category_name) VALUES('''
                             + category_id +', "' + category_name +'''")
                ''')
            conn.close()

    def insertDatabaseImageItem(self, databaseImageItem):
        conn = sqlite3.connect(self.__database_path)
        conn.execute('''
        INSERT INTO image(image_id, image_name, image_url, image_path, image_thumb_path, image_checksum, image_category_id)
        VALUES (
                NULL, {image_name}, {image_url}, {image_path}, {image_thumb_path}, {image_checksum}, {image_category_id}
        )
        '''.format(
                   image_name = databaseImageItem.image_name,
                   image_url = databaseImageItem.image_url,
                   image_path = databaseImageItem.image_path,
                   image_thumb_path = databaseImageItem.image_thumb_path,
                   image_checksum = databaseImageItem.image_checksum,
                   image_category_id = databaseImageItem.image_category_id))
        conn.close()

__author__ = 'tropsci'

class ImageDatabaseItem:

    def __init__(self, _image_name, _image_url, _image_path, _image_thumb_path, _image_checksum, _image_category_name):
        self.image_name = _image_name
        self.image_url = _image_url
        self.image_path = _image_path
        self.image_thumb_path = _image_thumb_path
        self.image_checksum = _image_checksum
        self.image_category_name = _image_category_name

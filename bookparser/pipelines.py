# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient

class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books_from_sites

    def process_item(self, item, spider):
        if spider.name == 'labirintru':
            if item.get('old_price') is not None:
                item['old_price'] = int(item.get('old_price'))
            if item.get('price') is not None:
                item['price'] = int(item.get('price'))
            if item.get('rating') is not None:
                item['rating'] = float(item.get('rating'))
        else:
            if item.get('price') is not None:
                item['price'] = int(item.get('price'))
            if item.get('old_price') is not None:
                item['old_price'] = int(item.get('old_price')[:-2])
            if item.get('rating') is not None:
                item['rating'] = float(item.get('rating').replace(",", "."))

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

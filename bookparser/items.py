# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookparserItem(scrapy.Item):
    # для обоих поля одинаковые
    link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    old_price = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()


# class LabirintruItem(scrapy.Item):
#     link = scrapy.Field()
#     name = scrapy.Field()
#     author = scrapy.Field()
#     old_price = scrapy.Field()
#     price = scrapy.Field()
#     rating = scrapy.Field()
#     _id = scrapy.Field()
#
# class Book24ruItem(scrapy.Item):
#     link = scrapy.Field()
#     name = scrapy.Field()
#     author = scrapy.Field()
#     old_price = scrapy.Field()
#     price = scrapy.Field()
#     rating = scrapy.Field()
#     _id = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def change_url(value):
    try:
        result = value.replace('_s', '_b')
        return result
    except Exception:
        return value


def clear(value):
    try:
        result = value.replace(' ', '').replace('\n','')
        return result
    except Exception:
        return value


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    photos = scrapy.Field()
    price = scrapy.Field()
    parameters = scrapy.Field()

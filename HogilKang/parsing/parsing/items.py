# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsingItem(scrapy.Item):
    title = scrapy.Field()
    writer = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    media = scrapy.Field()
    update_at = scrapy.Field()

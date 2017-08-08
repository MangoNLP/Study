# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ParsingPipeline(object):

    def open_spider(self, spider):
        self.f = open('test.txt', 'a', encoding='utf8')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        line = str(dict(item))
        self.f.write(line + '\n')
        return item

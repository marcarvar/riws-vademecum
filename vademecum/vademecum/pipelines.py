# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class VademecumPipeline:
    
    def open_spider(self , spider):
        self.listItem = []
        
    def close_spider(self, spider):
        with open(spider.name + '.json', 'w') as outfile:
            json.dump(self.listItem, outfile)

    def process_item(self, item, spider):
        self.listItem.append(dict(item))
        return item

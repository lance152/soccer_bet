# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class GetDataPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.insert(postItem)  # 向数据库插入一条记录
        return item

class DailyDataPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['info']  # 获得数据库的句柄
        self.coll = self.db['daily']
        self.coll.drop()

    def process_item(self,item,spider):
        if item['peilv_win_final_Bet365'] != 0:
            postItem = dict(item)
            self.coll.insert(postItem)  # 向数据库插入一条记录

            return item
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from get_data.items import getCoarseData
from get_data.spiders.processData import get_inside

class DenmarkSpider(scrapy.Spider):
    name = 'Denmark'
    allowed_domains = ['500.com']

    saiji_list = [11744, 9859, 8747, 7499, 6917, 6126, 5437, 4841, 4049, 3294, 2668, 991, 829, 653, 364, 237, 539, 323]
    saiji_name = ['1718', '1617', '1516', '1415', '1314', '1213', '1112', '1011', '0910', '0809', '0708', '0607', '0506', '0405', '0304', '0203', '0102', '0001']

    def start_requests(self):
        for saiji in self.saiji_list:
            for round in range(1,27):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid={}&round={}'.format(saiji,round)

                yield Request(url=url,callback=self.parse,meta={'saiji':self.saiji_name[self.saiji_list.index(saiji)]})

    def parse(self, response):
        data = json.loads(response.text)

        for i in data:
            id = i['fid']
            url = 'http://odds.500.com/fenxi/ouzhi-%s.shtml' % id

            info = {}
            info['round'] = int(i['round'])
            info['saiji'] = response.meta['saiji']
            info['hscore'] = int(i['hscore'])
            info['gscore'] = int(i['gscore'])
            info['hname'] = i['hname']
            info['gname'] = i['gname']
            info['fid'] = id

            yield Request(url=url,callback=self.get_data,meta=info)

    def get_data(self,response):
        item = getCoarseData()

        i = 1
        for key in response.meta:
            if i < 8:
                item[key] = response.meta[key]
                i += 1

        company_list = {'Bet365':3}

        get_inside('peilv', company_list, response, item)

        return item


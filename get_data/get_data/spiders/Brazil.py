# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from get_data.items import getCoarseData
from get_data.spiders.processData import get_inside

class SwedenSpider(scrapy.Spider):
    name = 'Brazil'
    allowed_domains = ['500.com']

    saiji_list = [11455, 9594, 8333, 7348, 6744, 6025, 5287, 4626, 3914, 3214, 2355, 925]

    saiji_name = ['17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07', '06']

    def start_requests(self):
        for saiji in self.saiji_list:
            for round in range(1,39):
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
            if i['hscore'] and i['gscore']:
                info['hscore'] = int(i['hscore'])
                info['gscore'] = int(i['gscore'])
            else:
                info['hscore'] = -1
                info['gscore'] = -1
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

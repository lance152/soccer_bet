# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from get_data.items import GetDataItem
from scrapy.selector import Selector

class GermanySpider(scrapy.Spider):
    name = 'Germany'
    allowed_domains = ['500.com']
    saiji_list = [11826, 10077, 8739, 7479, 6830, 6135]
    #saiji_list = [11826]
    saiji_name = [17_18, 16_17, 15_16, 14_15, 13_14, 12_13]
    def start_requests(self):
        for i in self.saiji_list:
            for j in range(1,35):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid={}&round={}'.format(i,j)
                yield Request(url=url,callback=self.parse,meta={'saiji':self.saiji_name[self.saiji_list.index(i)]})

    def parse(self, response):
        data = json.loads(response.text)
        for i in data:
            id = i['fid']
            url = 'http://odds.500.com/fenxi/ouzhi-%s.shtml' % id

            info = {}
            info['round'] = float(i['round'])
            info['saiji'] = response.meta['saiji']
            info['hscore'] = float(i['hscore'])
            info['gscore'] = float(i['gscore'])
            info['hname'] = i['hname']
            info['gname'] = i['gname']

            yield Request(url=url,callback=self.get_kaili,meta=info)

    def get_kaili(self,response):
        item = GetDataItem()
        item['round'] = response.meta['round']
        item['saiji'] = response.meta['saiji']
        item['hscore'] = response.meta['hscore']
        item['gscore'] = response.meta['gscore']
        item['hname'] = response.meta['hname']
        item['gname'] = response.meta['gname']

        item['kaili_win_start'] = 0
        item['kaili_draw_start'] = 0
        item['kaili_lose_start'] = 0

        item['kaili_win_final'] = 0
        item['kaili_draw_final'] = 0
        item['kaili_lose_final'] = 0

        # 初赔
        item['win_start'] = 0
        item['draw_start'] = 0
        item['lose_start'] = 0

        item['win_final'] = 0
        item['draw_final'] = 0
        item['lose_final'] = 0

        item['fanli_start'] = 0
        item['fanli_final'] = 0

        odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[1]/td/text()').extract()
        print(type(odds))
        if len(odds) != 0:
            odds = list(map(float, odds))
            item['kaili_win_start'] = odds[0]
            item['kaili_draw_start'] = odds[1]
            item['kaili_lose_start'] = odds[2]

        odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()').extract()
        print(type(odds))
        if len(odds) != 0:
            odds = list(map(float, odds))
            item['kaili_win_final'] = odds[0]
            item['kaili_draw_final'] = odds[1]
            item['kaili_lose_final'] = odds[2]

        odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()').extract()
        if len(odds) != 0:
            odds = list(map(float, odds))
            item['win_start'] = odds[0]
            item['draw_start'] = odds[1]
            item['lose_start'] = odds[2]

        odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[2]/td/text()').extract()
        odds = [x.strip() for x in odds]
        if len(odds) != 0:
            odds = list(map(float, odds))
            item['win_final'] = odds[0]
            item['draw_final'] = odds[1]
            item['lose_final'] = odds[2]

        fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[1]/td/text()').extract()
        fanli = [x.replace('%', '') for x in fanli]
        if len(fanli) != 0:
            fanli = list(map(float, fanli))
            item['fanli_start'] = fanli[0]

        fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[2]/td/text()').extract()
        fanli = [x.replace('%', '') for x in fanli]
        if len(fanli) != 0:
            fanli = list(map(float, fanli))
            item['fanli_final'] = fanli[0]

        return item
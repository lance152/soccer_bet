# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from get_data.items import GetDataItem

class GermanySpider(scrapy.Spider):
    name = 'Germany'
    allowed_domains = ['500.com']
    saiji_list = [11826, 10077, 8739, 7479, 6830, 6135]
    #saiji_list = [6135]
    saiji_name = [1718, 1617, 1516, 1415, 1314, 1213]
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
            info['round'] = int(i['round'])
            info['saiji'] = response.meta['saiji']
            info['hscore'] = int(i['hscore'])
            info['gscore'] = int(i['gscore'])
            info['hname'] = i['hname']
            info['gname'] = i['gname']
            info['fid'] = id

            yield Request(url=url,callback=self.get_kaili,meta=info)

    def get_kaili(self,response):
        item = GetDataItem()
        # item['round'] = response.meta['round']
        # item['saiji'] = response.meta['saiji']
        # item['hscore'] = response.meta['hscore']
        # item['gscore'] = response.meta['gscore']
        # item['hname'] = response.meta['hname']
        # item['gname'] = response.meta['gname']

        #获取比赛常规数据
        i=1
        for key in response.meta:
            if i < 8:
                item[key] = response.meta[key]
                i += 1

        company_list = {'William':293,'Bet365':3}
        #odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[1]/td/text()').extract()
        # set_kaili('start','William',response,item)
        # set_kaili('start', 'Bet365', response, item)
        get_inside('kaili',company_list,response,item)
        #odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()').extract()
        # set_kaili('final','William',response,item)
        # set_kaili('final','Bet365',response,item)

        #odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[1]/td/text()').extract()
        # set_peilv('start', 'William', response, item)
        # set_peilv('start', 'Bet365', response, item)
        get_inside('peilv',company_list,response,item)

        #odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[2]/td/text()').extract()
        # set_peilv('final', 'William', response, item)
        # set_peilv('final', 'Bet365', response, item)

        #fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[1]/td/text()').extract()
        # set_fanli('start','William',response,item)
        # set_fanli('start','Bet365',response,item)
        get_inside('fanli',company_list,response,item)

        #fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[2]/td/text()').extract()
        # set_fanli('final', 'William', response, item)
        # set_fanli('final','Bet365',response,item)

        return item
        #print(item)

def get_inside(cata,company_list,response,item):
    for company in company_list:
        id = company_list[company]
        if cata == 'kaili':
            td = 6
        elif cata == 'peilv':
            td = 3
        elif cata == 'fanli':
            td = 5
        odds_start = response.xpath('//*[@id="%s"]/td[%s]/table/tbody/tr[1]/td/text()' % (id, td)).extract()
        odds_final = response.xpath('//*[@id="%s"]/td[%s]/table/tbody/tr[2]/td/text()' % (id, td)).extract()
        process_data(odds_start, item, cata, 'start', company)
        process_data(odds_final, item, cata, 'final', company)

def process_data(odds,item,cata,time,company):
    if len(odds)==3:
        odds = [x.strip() for x in odds]
        odds = list(map(float, odds))
        item['%s_win_%s_%s' % (cata,time,company)] = odds[0]
        item['%s_draw_%s_%s' % (cata,time,company)] = odds[1]
        item['%s_lose_%s_%s' % (cata,time,company)] = odds[2]
    elif len(odds)==0:
        if cata == 'fanli':
            item['fanli_%s_%s' % (time, company)] = 0
        else:
            item['%s_win_%s_%s' % (cata,time,company)] = 0
            item['%s_draw_%s_%s' % (cata,time,company)] = 0
            item['%s_lose_%s_%s' % (cata,time,company)] = 0

    elif len(odds)==1:
        odds = [x.replace('%', '') for x in odds]
        odds = list(map(float, odds))
        item['%s_%s_%s' % (cata, time,company)] = odds[0]

# def set_kaili(cata,company,response,item):
#     if company == 'William' and cata == 'start':
#         odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[1]/td/text()').extract()
#     elif company == 'Bet365' and cata == 'start':
#         odds = response.xpath('//*[@id="3"]/td[6]/table/tbody/tr[1]/td/text()').extract()
#     elif company == 'William' and cata == 'final':
#         odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()').extract()
#     elif company == 'Bet365' and cata == 'final':
#         odds = response.xpath('//*[@id="3"]/td[6]/table/tbody/tr[2]/td/text()').extract()
#
#     if odds:
#         odds = list(map(float, odds))
#         item['kaili_win_%s_%s' % (cata,company)] = odds[0]
#         item['kaili_draw_%s_%s' % (cata,company)] = odds[1]
#         item['kaili_lose_%s_%s' % (cata,company)] = odds[2]
#     else:
#         item['kaili_win_%s_%s' % (cata,company)] = 0
#         item['kaili_draw_%s_%s' % (cata,company)] = 0
#         item['kaili_lose_%s_%s' % (cata,company)] = 0
#
# def set_peilv(cata,company,response,item):
#     if company == 'William' and cata == 'start':
#         odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[1]/td/text()').extract()
#     elif company == 'Bet365' and cata == 'start':
#         odds = response.xpath('//*[@id="3"]/td[3]/table/tbody/tr[1]/td/text()').extract()
#     elif company == 'William' and cata == 'final':
#         odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[2]/td/text()').extract()
#     elif company == 'Bet365' and cata == 'final':
#         odds = response.xpath('//*[@id="3"]/td[3]/table/tbody/tr[2]/td/text()').extract()
#
#     if odds:
#         odds = [x.strip() for x in odds]
#         odds = list(map(float, odds))
#         item['peilv_win_%s_%s' % (cata,company)] = odds[0]
#         item['peilv_draw_%s_%s' % (cata,company)] = odds[1]
#         item['peilv_lose_%s_%s' % (cata,company)] = odds[2]
#     else:
#         item['peilv_win_%s_%s' % (cata,company)] = 0
#         item['peilv_draw_%s_%s' % (cata,company)] = 0
#         item['peilv_lose_%s_%s' % (cata,company)] = 0
#
# def set_fanli(cata,company,response,item):
#     if company == 'William' and cata == 'start':
#         fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[1]/td/text()').extract()
#     elif company == 'Bet365' and cata == 'start':
#         fanli = response.xpath('//*[@id="3"]/td[5]/table/tbody/tr[1]/td/text()').extract()
#     elif company == 'William' and cata == 'final':
#         fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[2]/td/text()').extract()
#     elif company == 'Bet365' and cata == 'final':
#         fanli = response.xpath('//*[@id="3"]/td[5]/table/tbody/tr[2]/td/text()').extract()
#     if fanli:
#         fanli = [x.replace('%', '') for x in fanli]
#         fanli = list(map(float, fanli))
#         item['fanli_%s_%s' % (cata,company)] = fanli[0]
#     else:
#         item['fanli_%s_%s' % (cata, company)] = 0
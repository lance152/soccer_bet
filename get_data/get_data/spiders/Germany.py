# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from get_data.items import getCoarseData
from get_data.spiders.processData import get_inside

class GermanySpider(scrapy.Spider):
    name = 'Germany'
    allowed_domains = ['500.com']
    saiji_list = [11826, 10077, 8739, 7479, 6830, 6135, 5438, 4820, 4070, 3308, 2652, 970, 841, 646, 290, 533, 242, 186]

    #saiji_list = [6135]
    saiji_name = ['1718', '1617', '1516', '1415', '1314', '1213', '1112', '1011', '0910', '0809', '0708', '0607', '0506', '0405',
     '0304', '0203', '0102', '0001']

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'get_data.pipelines.GetDataPipeline': 1
    #     }
    # }

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
        item = getCoarseData()
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

        #company_list = {'William':293,'Bet365':3}
        company_list = {'Bet365':3}
        # #odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[1]/td/text()').extract()
        # # set_kaili('start','William',response,item)
        # # set_kaili('start', 'Bet365', response, item)
        # get_inside('kaili',company_list,response,item)
        # #odds = response.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()').extract()
        # # set_kaili('final','William',response,item)
        # # set_kaili('final','Bet365',response,item)
        #
        # #odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[1]/td/text()').extract()
        # # set_peilv('start', 'William', response, item)
        # # set_peilv('start', 'Bet365', response, item)
        get_inside('peilv',company_list,response,item)
        #
        # #odds = response.xpath('//*[@id="293"]/td[3]/table/tbody/tr[2]/td/text()').extract()
        # # set_peilv('final', 'William', response, item)
        # # set_peilv('final', 'Bet365', response, item)
        #
        # #fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[1]/td/text()').extract()
        # # set_fanli('start','William',response,item)
        # # set_fanli('start','Bet365',response,item)
        # get_inside('fanli',company_list,response,item)
        #
        # #fanli = response.xpath('//*[@id="293"]/td[5]/table/tbody/tr[2]/td/text()').extract()
        # # set_fanli('final', 'William', response, item)
        # # set_fanli('final','Bet365',response,item)

        return item
        #print(item)

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
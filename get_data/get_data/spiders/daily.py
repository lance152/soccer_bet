# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from get_data.items import dailyDataItem
from get_data.spiders.processData import get_inside

class DailySpider(scrapy.Spider):
    name = 'daily'
    allowed_domains = ['500.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'get_data.pipelines.DailyDataPipeline': 1
        }
    }
    def start_requests(self):

        for i in range(1,23):
            if i < 10 :
                url_base = 'http://live.500.com/wanchang.php?e=2018-07-0'
            else:
                url_base = 'http://live.500.com/wanchang.php?e=2018-07-'
            url = url_base + str(i)

            yield Request(url=url,callback=self.parse,meta={'date':i})

    def parse(self, response):
        content = response.xpath('//*[@id="table_match"]/tbody/tr')
        info = {}
        info['date'] = 7+response.meta['date']/100
        for i in content:
            if i.xpath('@id').extract():
                info['hname'] = i.xpath('td[5]/a/span/text()').extract()[0]
                info['gname'] = i.xpath('td[7]/a/span/text()').extract()[0]

                data_h = i.xpath('td[6]/div/a[1]/text()').extract()
                data_g = i.xpath('td[6]/div/a[3]/text()').extract()
                if data_h and data_g:
                    info['hscore'] = int(data_h[0])
                    info['gscore'] = int(data_g[0])
                else:
                    info['hscore'] = -1
                    info['gscore'] = -1

                link = i.xpath('td[9]/a[3]/@href').extract()[0]

                info['time'] = i.xpath('td[3]/text()').extract()[0]

                url_head = 'http:'
                url = url_head + link

                yield Request(url=url,callback=self.get_ouzhi,meta=info)

    def get_ouzhi(self,response):
        item = dailyDataItem()

        i = 1
        for key in response.meta:
            if i < 7:
                item[key] = response.meta[key]
                i += 1

        company_list = {'Bet365':3}

        get_inside('peilv',company_list,response,item)

        return item
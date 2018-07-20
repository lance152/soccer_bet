# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetDataItem(scrapy.Item):
    #轮数
    round = scrapy.Field()

    #赛季
    saiji = scrapy.Field()

    #进球数
    hscore = scrapy.Field()
    gscore = scrapy.Field()

    #队名
    hname = scrapy.Field()
    gname = scrapy.Field()

    #初赔
    win_start = scrapy.Field()
    draw_start = scrapy.Field()
    lose_start = scrapy.Field()

    #临盘
    win_final = scrapy.Field()
    draw_final = scrapy.Field()
    lose_final = scrapy.Field()

    #返利率
    fanli_start = scrapy.Field()
    fanli_final = scrapy.Field()

    #初赔凯利
    kaili_win_start = scrapy.Field()
    kaili_draw_start = scrapy.Field()
    kaili_lose_start = scrapy.Field()

    #临盘凯利
    kaili_win_final = scrapy.Field()
    kaili_draw_final = scrapy.Field()
    kaili_lose_final = scrapy.Field()
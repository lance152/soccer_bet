# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetDataItem(scrapy.Item):
    #比赛编号
    fid = scrapy.Field()

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

    #初赔_威廉希尔
    peilv_win_start_William = scrapy.Field()
    peilv_draw_start_William  = scrapy.Field()
    peilv_lose_start_William  = scrapy.Field()

    #临盘_威廉希尔
    peilv_win_final_William  = scrapy.Field()
    peilv_draw_final_William  = scrapy.Field()
    peilv_lose_final_William  = scrapy.Field()

    #返利率_威廉希尔
    fanli_start_William  = scrapy.Field()
    fanli_final_William  = scrapy.Field()

    #初赔凯利_威廉希尔
    kaili_win_start_William  = scrapy.Field()
    kaili_draw_start_William  = scrapy.Field()
    kaili_lose_start_William  = scrapy.Field()

    #临盘凯利_威廉希尔
    kaili_win_final_William  = scrapy.Field()
    kaili_draw_final_William  = scrapy.Field()
    kaili_lose_final_William  = scrapy.Field()

    #初赔_Bet365
    peilv_win_start_Bet365 = scrapy.Field()
    peilv_draw_start_Bet365  = scrapy.Field()
    peilv_lose_start_Bet365  = scrapy.Field()

    #临盘_Bet365
    peilv_win_final_Bet365  = scrapy.Field()
    peilv_draw_final_Bet365  = scrapy.Field()
    peilv_lose_final_Bet365  = scrapy.Field()

    #返利率_Bet365
    fanli_start_Bet365  = scrapy.Field()
    fanli_final_Bet365  = scrapy.Field()

    #初赔凯利_Bet365
    kaili_win_start_Bet365  = scrapy.Field()
    kaili_draw_start_Bet365  = scrapy.Field()
    kaili_lose_start_Bet365  = scrapy.Field()

    #临盘凯利_Bet365
    kaili_win_final_Bet365  = scrapy.Field()
    kaili_draw_final_Bet365  = scrapy.Field()
    kaili_lose_final_Bet365  = scrapy.Field()
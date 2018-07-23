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
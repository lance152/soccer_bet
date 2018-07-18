from pymongo import MongoClient
import requests
import json
from lxml import etree

saiji_list = [11826,10077,8739,7479,6830,6135]
#saiji_list = [11826]
saiji_name = [17_18,16_17,15_16,14_15,13_14,12_13]

def reset_db():
    client = MongoClient()
    client.drop_database('Germany')

def initilize_db():
    Client = MongoClient()
    db = Client['Germany']

    return db

def get_collection(saiji,db):

    return db['Saiji'+str(saiji_name[saiji_list.index(saiji)])]

def get_url(saiji,round):

    return 'http://liansai.500.com/index.php?c=score&a=getmatch&stid={}&round={}'.format(saiji,round)

def get_info(url):
    #抓取主要信息
    re = requests.get(url)
    data = json.loads(re.text)

    #抓取凯利值信息
    for game in data:
        id = game['fid']
        url = 'http://odds.500.com/fenxi/ouzhi-%s.shtml' % id
        re = requests.get(url).text
        content = etree.HTML(re)
        game['kaili_win_start'] = 0
        game['kaili_draw_start'] = 0
        game['kaili_lose_start'] = 0

        game['kaili_win_final'] = 0
        game['kaili_draw_final'] = 0
        game['kaili_lose_final'] = 0
        odds = content.xpath('//*[@id="293"]/td[6]/table/tbody/tr[1]/td/text()')
        if len(odds) != 0:
            odds = list(map(float, odds))
            game['kaili_win_start'] = odds[0]
            game['kaili_draw_start'] = odds[1]
            game['kaili_lose_start'] = odds[2]

        odds = content.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()')
        if len(odds) != 0:
            odds = list(map(float, odds))
            game['kaili_win_final'] = odds[0]
            game['kaili_draw_final'] = odds[1]
            game['kaili_lose_final'] = odds[2]
    return data

def write_data(data,col):
    col.insert_one(data)

def run():
    reset_db()
    db = initilize_db()
    for x in saiji_list:
        print('Start ' + str(saiji_name[saiji_list.index(x)]) + '赛季')
        col = get_collection(x, db)
        for i in range(1,35):
            print('Start Round ' + str(i))
            url = get_url(x,i)
            data = get_info(url)
            for s in data:
                write_data(s,col)
            print('Round ' + str(i) + " Done")
            print('*'*40)

if __name__ == "__main__":
    run()
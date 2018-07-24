from pymongo import MongoClient
import matplotlib.pyplot as plt
import statistics
import requests
from lxml import etree

MONEY = 10
count = 0
bingo = []
bet_count = 0
max_bingo = 0
min_bingo = 9
def initilize_db():
    Client = MongoClient()
    db = Client['Germany']

    return db

def get_collection(db,saiji=1718):

    return db['Saiji'+str(saiji)]

def get_data(col,round):

    return col.find({'round': str(round)})

def get_kaili(id):
    url = 'http://odds.500.com/fenxi/ouzhi-%s.shtml' % id
    re = requests.get(url).text
    content = etree.HTML(re)
    odds = content.xpath('//*[@id="293"]/td[6]/table/tbody/tr[2]/td/text()')
    odds = list(map(float,odds))
    return odds

def bet(money):
    # best = round(money/11,2)
    # if best > 2500:
    #     return 2500
    # return best
    return 0.1*MONEY
    # if money < 9:
    #     return 10-money
    # return 1

def cold(result,money,odds,kaili=[]):
    chosen = max(odds)
    global count
    global bingo
    #paid = bet(money)
    # money -= paid
    if result == chosen:
        count +=1
        bingo.append(chosen)
        return round(money*chosen,2)

    return 0

def kl(result,money,odds,kai_li):
    if len(kai_li)==0:
        return bet(money)
    chosen = odds[kai_li.index(min(kai_li))]
    if chosen < 3:
        return bet(money)
    global count
    global bingo
    global bet_count

    bet_count += 1
    #paid = bet(money)
    # money -= paid
    if result == chosen:
        count +=1
        bingo.append(chosen)
        return round(money*chosen,2)

    return 0

def nothot(result,money,odds):
    chosen = max(odds)

    global count
    global bingo

    if result != min(odds):
        count += 1
        bingo.append(result)
        return round(money/2 * result,2)
    return 0

def host(result,money,odds):
    chosen = odds[0]
    global count
    global bingo
    #paid = bet(money)
    # money -= paid
    if result == chosen:
        count +=1
        bingo.append(chosen)
        return round(money*chosen,2)

    return 0

def hot(result,money,odds):
    chosen = min(odds)
    global count
    global bingo
    #paid = bet(money)
    # money -= paid
    if result == chosen:
        count +=1
        bingo.append(chosen)
        return round(money*chosen,2)

    return 0

def mid(result,money,odds):
    chosen = sorted(odds)[1]
    global count
    global bingo
    #paid = bet(money)
    # money -= paid
    if result == chosen:
        count +=1
        bingo.append(chosen)
        return round(money*chosen,2)

    return 0

def play(game,Money,strategy,kai_li):
    win = float(game['win'])
    draw = float(game['draw'])
    lost = float(game['lost'])

    odds = [win, draw, lost]

    if float(game['hscore']) > float(game['gscore']):
        return strategy(win, Money, odds,kai_li)
    elif float(game['hscore']) < float(game['gscore']):
        return strategy(lost, Money, odds,kai_li)
    else:
        return strategy(draw, Money, odds,kai_li)

def pic(data):
    x = range(len(data))
    plt.figure()
    #plt.figure(figsize=(15, 10))
    plt.plot(x,data)


def run():
    global count
    global bet_count
    global max_bingo
    global min_bingo
    Money = MONEY #初始资金
    Money_flow = [Money]
    counts=[]
    db = initilize_db()
    col = get_collection(db,1617)

    for i in range(1,2):
        print('开始分析第' + str(i) + '轮！')
        games = get_data(col,i)
        paid = bet(Money)
        Money = round(Money-paid*9,2)
        #Money_flow.append(Money)
        for g in games:
            id = g['fid']
            kai_li = get_kaili(id)
            host = g['hname']
            guest = g['gname']
            print('开始分析 ' + host + ' 对阵 ' + guest + ' 的比赛')
            Money = round(play(g,paid,kl,kai_li)+Money,2)
            #print(Money)
        print(Money)
        Money_flow.append(Money)
        counts.append(round(count/bet_count,2))
        print('下注次数： ' + str(bet_count))
        print('猜中次数： ' + str(count))
        if count > max_bingo:
            max_bingo = count
        if count < min_bingo:
            min_bingo = count
        #print(counts)
        count=0
        bet_count = 0
        print('第' + str(i) + '轮分析完成！')
        print('-'*30)
    print(Money_flow)
    print('最低点: ' + str(min(Money_flow)))
    print('最高点: ' + str(max(Money_flow)))
    print('Final money: ' + str(Money))
    print('Average win rate: ' + str(round(statistics.mean(counts),2)))
    print('Average 赔率: ' + str(round(statistics.mean(bingo),2)))
    print('最少猜中场次： '  + str(min_bingo))
    print('最多猜中场次： ' + str(max_bingo))
    print(counts)
    pic(Money_flow)
    pic(counts)
    plt.show()

if __name__ == "__main__":
    plt.close('all')
    run()
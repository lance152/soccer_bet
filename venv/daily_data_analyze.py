#分析全压平局的胜率
from time import sleep

from pymongo import MongoClient
import statistics

MONEY = 100

def initilize_db():
    Client = MongoClient()
    db = Client['info']
    col = db['daily']

    return col

def get_games(day,col):

    date = 7+day/100
    return col.find({'date':date})

def get_result(game):
    if game['hscore'] > game['gscore']:
        return 3
    elif game['hscore'] < game['gscore']:
        return 0
    else:
        return 1

def isDrawHighOdds(odd):
    #if game['peilv_draw_final_Bet365'] > 2.618:
    if odd > 2.618:
        return True
    else:
        return False

def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def bet(n):

    return fib(n)

#def bet(money):

#    return round(0.1*money,2)

def run():
    col = initilize_db()

    money = MONEY

    money_flow = [money]
    total_odds = []
    total_bet = []
    bingos = []
    counts = []
    n = 1
    for i in range(1,23):
        print('开始分析 7月' + str(i) + '日 的比赛')

        games = get_games(i,col)

        day_bingo = 0
        day_count = 0
        odds = []
        day_bet = bet(n)
        for g in games:
            host = g['hname']
            guest = g['gname']
            #print('开始分析 ' + host + ' 对阵 ' + guest + ' 的比赛')
            result = get_result(g)
            odd = g['peilv_draw_final_Bet365']

            if isDrawHighOdds(odd):
                day_bingo += 1
                money -= day_bet
                total_odds.append(odd)
                total_bet.append(day_bet)

            if result == 1:
                day_count += 1
                money += day_bet*odd
                money = round(money,2)
                odds.append(odd)



        print('本日下注次数： ' + str(day_bingo))
        print('本日猜中次数： ' + str(day_count))
        print('本日剩余资金： ' + str(round(money,2)))
        print('本日下注额： ' + str(day_bet))
        print('本日赔率： ' + str(odds))
        if day_bingo != 0:
            print('本轮胜率： ' + str(round(day_count/day_bingo,2)))
        else:
            print('没下注')
        print('*'*20)
        money_flow.append(money)
        bingos.append(day_bingo)
        counts.append(day_count)

        if money > MONEY:
            n -= 2
            if n < 1:
                n = 1
        n += 1

    print('总下注场数： ' + str(sum(bingos)))
    print('总猜中场数： ' + str(sum(counts)))
    print('平均赔率： ' + str(round(statistics.mean(total_odds),2)))
    print('平均下注额： ' + str(round(statistics.mean(total_bet),2)))
    print(money)
    print(money_flow)

if __name__ == '__main__':
    # saiji = input('输入欲分析的赛季： ')
    # run(float(saiji))

    run()
#分析全压平局的胜率

from pymongo import MongoClient
import statistics

MONEY = 100

def initilize_db():
    Client = MongoClient()
    db = Client['info']
    col = db['Germany']

    return col

def get_games(saiji,round,col):

    return col.find({'round':round,'saiji':saiji})

def get_result(game):
    if game['hscore'] > game['gscore']:
        return 3
    elif game['hscore'] < game['gscore']:
        return 0
    else:
        return 1

def isDrawHighOdds(game):
    if game['draw_final'] > 2.618:
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

def run(saiji):
    col = initilize_db()
    #saiji = 1718

    print('开始分析 ' + str(saiji) + ' 赛季')
    counts = []
    bingos = []
    money = MONEY
    money_flow = []
    n = 1
    for i in range(1,35):
        print('开始分析第 ' + str(i) + ' 轮')

        games = get_games(saiji,i,col)
        round_count = 0
        round_bingo = 0
        if money < MONEY:
            n += 1
        else:
            n -= 2
            if n < 1:
                n = 1
        round_bet = bet(n)

        odds = []
        for g in games:
            host = g['hname']
            guest = g['gname']
            print('开始分析 ' + host + ' 对阵 ' + guest + ' 的比赛')
            result = get_result(g)

            if isDrawHighOdds(g):
                round_bingo += 1
                money -= round_bet

            if result == 1:
                round_count += 1
                odd = g['draw_final']
                money += round(round_bet*odd,2)
                odds.append(odd)

        print('本轮下注次数： ' + str(round_bingo))
        print('本轮猜中次数： ' + str(round_count))
        print('本轮剩余资金： ' + str(money))
        print('本轮下注额： ' + str(round_bet))
        print('本轮赔率： ' + str(odds))
        if round_bingo != 0:
            print('本轮胜率： ' + str(round(round_count/round_bingo,2)))
        else:
            print('没下注')
        counts.append(round_count)
        bingos.append(round_bingo)
        money_flow.append(money)
        print('完成分析第 ' + str(i) + ' 轮')
        print('*'*20)

    print('总胜率： ' + str(round(sum(counts)/sum(bingos),2)))
    print(money)
    money_flow = [round(x,2) for x in money_flow]
    print(money_flow)

if __name__ == '__main__':
    saiji = input('输入欲分析的赛季： ')
    print(fib(5))
    run(float(saiji))

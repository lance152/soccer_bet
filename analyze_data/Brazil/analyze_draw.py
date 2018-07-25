from time import sleep

from pymongo import MongoClient
import statistics

MONEY = 100

def initilize_db():
    Client = MongoClient()
    db = Client['info']
    col = db['Brazil']

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

def run(saiji):
    col = initilize_db()
    saiji_bingo = []
    saiji_count = []
    saiji_odd = []
    saiji_bet = []

    money = MONEY
    money_flow = [money]
    #print('开始分析 ' + str(saiji) + ' 赛季')

    n = 1

    for i in range(1,39):
        round_bingo = 0
        round_count = 0
        #print('开始分析第 ' + str(i) + ' 轮')

        games = get_games(saiji,i,col)

        round_bet = bet(n)

        for g in games:
            host = g['hname']
            guest = g['gname']

            result = get_result(g)
            odd = g['peilv_draw_final_Bet365']

            if isDrawHighOdds(odd):
                round_count += 1
                money -= round_bet
                saiji_bet.append(round_bet)

            #print(host + ' 对阵 ' + guest + '-'*5 + str(result))

            if result == 1:
                round_bingo += 1
                saiji_odd.append(odd)
                money += round(round_bet*odd,2)

        #print('本轮猜中次数： ' + str(round_bingo))
        saiji_bingo.append(round_bingo)
        saiji_count.append(round_count)
        #print('完成分析第 ' + str(i) + ' 轮')
        #print('*'*20)
        money_flow.append(money)

        if money > MONEY:
            n -= 2
            if n < 1:
                n = 1
        n += 1

    print(saiji + ' 赛季数据')
    print('本赛季下注场数： ' + str(sum(saiji_count)))
    print('本赛季猜中次数： ' + str(sum(saiji_bingo)))
    print('本赛季胜率: ' + str(round(sum(saiji_bingo)/sum(saiji_count),2)))
    print('平均赔率： ' + str(round(statistics.mean(saiji_odd),2)))
    print('平均下注额： ' + str(round(statistics.mean(saiji_bet),2)))
    # print(str(len(saiji_odd)))
    print('剩余资金: ' + str(round(money,2)))
    money_flow = [round(x,2) for x in money_flow]
    print(money_flow)
    print('*'*20)



if __name__ == '__main__':
    saiji_name = ['17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07', '06']
    #saiji_name = ['17']
    for i in saiji_name:
        run(i)
        #sleep(5)
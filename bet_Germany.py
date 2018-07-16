from pymongo import MongoClient
import matplotlib.pyplot as plt
import statistics

MONEY = 10
count = 0
bingo = []
def initilize_db():
    Client = MongoClient()
    db = Client['Germany']

    return db

def get_collection(db,saiji=1718):

    return db['Saiji'+str(saiji)]

def get_data(col,round):

    return col.find({'round': str(round)})

def bet(money):
    # best = round(money/11,2)
    # if best > 2500:
    #     return 2500
    # return best
    #return 0.1*MONEY
    if money < 9:
        return 10-money
    return 1

def cold(result,money,odds):
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
def play(game,Money,strategy):
    win = float(game['win'])
    draw = float(game['draw'])
    lost = float(game['lost'])

    odds = [win, draw, lost]

    if float(game['hscore']) > float(game['gscore']):
        return strategy(win, Money, odds)
    elif float(game['hscore']) < float(game['gscore']):
        return strategy(lost, Money, odds)
    else:
        return strategy(draw, Money, odds)

def pic(data):
    x = range(len(data))
    plt.figure()
    #plt.figure(figsize=(15, 10))
    plt.plot(x,data)


def run():
    global count
    Money = MONEY #初始资金
    Money_flow = [Money]
    counts=[]
    db = initilize_db()
    col = get_collection(db,1617)

    for i in range(1,2):
        games = get_data(col,i)
        paid = bet(Money)
        Money = round(Money-paid*9,2)
        Money_flow.append(Money)
        for g in games:

            Money = round(play(g,paid,cold)+Money,2)
            #print(Money)
        Money_flow.append(Money)
        counts.append(count)
        print(count)
        #print(counts)
        count=0
    print(Money_flow)
    print('最低点: ' + str(min(Money_flow)))
    print('最高点: ' + str(max(Money_flow)))
    print('Final money: ' + str(Money))
    print('Average win rate: ' + str(round(statistics.mean(counts)/9,2)))
    print('Average 赔率: ' + str(round(statistics.mean(bingo),2)))
    print('最少猜中场次： '  + str(min(counts)))
    print('最多猜中场次： ' + str(max(counts)))
    print(counts)
    pic(Money_flow)
    pic(counts)
    plt.show()

if __name__ == "__main__":
    plt.close('all')
    run()
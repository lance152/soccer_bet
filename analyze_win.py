from pymongo import MongoClient
import statistics


def initilize_db():
    Client = MongoClient()
    db = Client['Germany']

    return db

def get_collection(db,saiji=1718):

    return db['Saiji'+str(saiji)]

def get_data(col,round):

    return col.find({'round': str(round)})

def get_result(game):
    if float(game['hscore']) > float(game['gscore']):
        return 0
    elif float(game['hscore']) < float(game['gscore']):
        return 2
    else:
        return 1

def get_predict(game):
    kaili_win_diff = game['kaili_win_start'] - game['kaili_win_final']
    kaili_draw_diff = game['kaili_draw_start'] - game['kaili_draw_final']
    kaili_lose_diff = game['kaili_lose_start'] - game['kaili_lose_final']

    kaili = [kaili_win_diff,kaili_draw_diff,kaili_lose_diff]

    if len(list(set(kaili))) != 1:
        return kaili.index(max(kaili))
    else:
        return 3
def run():
    db = initilize_db()
    saiji = 1718
    col = get_collection(db,saiji)

    print('开始分析 ' + str(saiji) + ' 赛季')
    counts = []
    for i in range(1,35):
        print('开始分析第 ' + str(i) + ' 轮')

        games = get_data(col,i)
        round_count = 0
        for g in games:
            flag = False
            host = g['hname']
            guest = g['gname']
            result = get_result(g)
            predict = get_predict(g)

            if result == predict:
                round_count += 1
                flag = True

            if flag:
                print('完成分析 ' + host + ' 对阵 ' + guest + ' 的比赛' + '-'*5 + '中！')
            else:
                print('开始分析 ' + host + ' 对阵 ' + guest + ' 的比赛')
        print('本轮猜中次数： ' + str(round_count))
        counts.append(round_count)
        print('完成分析第 ' + str(i) + ' 轮')
        print('*'*20)

    #print(counts)
    print('平均猜中次数: ' + str(round(statistics.mean(counts),2)))
    rate = [round(counts[i]/9,2) for i in range(len(counts))]
    #print(rate)
    print('Average win rate: ' + str(round(statistics.mean(rate),2)))
if __name__ == '__main__':
    run()
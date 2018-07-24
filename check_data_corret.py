from pymongo import MongoClient

#saiji = [1718,1617,1516,1415,1314,1213]
saiji_name = ['1718', '1617', '1516', '1415', '1314', '1213', '1112', '1011', '0910', '0809', '0708', '0607', '0506', '0405',
     '0304', '0203', '0102', '0001']
def initialize_db():
    Client = MongoClient()
    db = Client['info']
    col = db['Germany']

    return col

def find_game(fid,col):

    return col.find_one({'fid':fid})

def show_data(game):
    data = '%s  %s  %s' %(game['peilv_win_final_Bet365'],game['peilv_draw_final_Bet365'],game['peilv_lose_final_Bet365'])
    print(data)

def count_check(col):
    for i in saiji_name:
        for j in range(1,35):
            count = col.find({'round':j,'saiji':i}).count()
            print(count)
            if count < 9:
                print(i)
                print(j)

if __name__ == '__main__':
    fid = input('Enter the game fid: ')

    col = initialize_db()
    game = find_game(fid,col)

    show_data(game)
    #count_check(col)

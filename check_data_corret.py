from pymongo import MongoClient

#saiji = [1718,1617,1516,1415,1314,1213]
saiji = [1213]
def initialize_db():
    Client = MongoClient()
    db = Client['info']
    col = db['Germany']

    return col

def find_game(fid,col):

    return col.find({'fid':fid})

def show_data(game):
    data = '%s  %s  %s  %s  %s  %s  %s' %(game['peilv_win_final'],game['peilv_draw_final'],game['peilv_lose_final'],
                                          game['fanli_final'],game['kaili_win_final'],game['kaili_draw_final'],
                                          game['kaili_lose_final'])
    print(data)

def count_check(col):
    for i in saiji:
        for j in range(1,35):
            count = col.find({'round':j,'saiji':i}).count()
            print(count)
            if count < 9:
                print(i)
                print(j)

if __name__ == '__main__':
    # fid = input('Enter the game fid: ')
    #
    col = initialize_db()
    # game = find_game(fid,col)
    #
    # show_data(game)
    count_check(col)

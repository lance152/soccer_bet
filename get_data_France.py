from pymongo import MongoClient
import requests
import json

saiji_list = [11740,9854,8701,7475,6831,6127]
saiji_name = [17_18,16_17,15_16,14_15,13_14,12_13]

def initilize_db():
    Client = MongoClient()
    db = Client['France']

    return db

def get_collection(saiji,db):

    return db['Saiji'+str(saiji_name[saiji_list.index(saiji)])]

def get_url(saiji,round):

    return 'http://liansai.500.com/index.php?c=score&a=getmatch&stid={}&round={}'.format(saiji,round)

def get_info(url):
    re = requests.get(url)
    data = json.loads(re.text)

    return data

def write_data(data,col):
    col.insert_one(data)

def run():
    db = initilize_db()
    for x in saiji_list:
        print('Start ' + str(saiji_name[saiji_list.index(x)]) + '赛季')
        col = get_collection(x, db)
        for i in range(1,39):
            print('Start Round ' + str(i))
            url = get_url(x,i)
            data = get_info(url)
            for s in data:
                write_data(s,col)
            print('Round ' + str(i) + " Done")

if __name__ == "__main__":
    run()
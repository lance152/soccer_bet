import requests
from lxml import etree
import matplotlib.pyplot as plt

MONEY = 10000

def get_games():

    url = 'http://www.500.com/worldcup/saicheng/xiaozusai/'

    re = requests.get(url)
    content = etree.HTML(re.text)

    h_score = content.xpath('//*[@class="score"]/i[1]/text()')
    g_score = content.xpath('//*[@class="score"]/i[2]/text()')

    odds = content.xpath('//*[@class="td-peilv"]/span/text()')

    games = []

    for i in range(len(h_score)):
        game = {}
        game['hgoal'] = h_score[i]
        game['ggoal'] = g_score[i]

        game['win'] = odds[3*i]
        game['draw'] = odds[3*i+1]
        game['lost'] = odds[3*i+2]
        games.append(game)

    return games

def cold(result,money,odds):
    chosen = max(odds)
    paid = bet(money)
    money -= paid
    if result == chosen:
        money += paid*chosen

    return money

def bet(money):

    return 0.1*money

def play(game,Money,strategy):
    win = float(game['win'])
    draw = float(game['draw'])
    lost = float(game['lost'])

    odds = [win, draw, lost]

    if float(game['hgoal']) > float(game['ggoal']):
        return strategy(win, Money, odds)
    elif float(game['hgoal']) < float(game['ggoal']):
        return strategy(lost, Money, odds)
    else:
        return strategy(draw, Money, odds)

def pic(data):
    x = range(len(data))
    #plt.figure(figsize=(15, 10))
    plt.plot(x,data)
    plt.show()

def run():
    Money = MONEY #初始资金
    Money_flow = [Money]

    games = get_games()

    for g in games:
        Money = play(g,Money,cold)
        Money_flow.append(Money)

    print(Money_flow)
    print(min(Money_flow))
    print(max(Money_flow))
    print(Money)
    pic(Money_flow)

if __name__ == "__main__":
    run()
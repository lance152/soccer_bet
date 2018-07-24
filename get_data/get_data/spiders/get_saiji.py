import requests
from lxml import etree
import re

def get_saiji_name1(saiji_list):
    saiji_name = []
    for i in range(1,len(saiji_list)+1):
        cur = 1718 - 101*(i-1)
        cur = str(cur).zfill(4)

        saiji_name.append(cur)

    return saiji_name

def get_saiji_name2(saiji_list):
    saiji_name = list(range(len(saiji_list)+1))
    saiji_name.sort(reverse=True)
    saiji_name = [str(x).zfill(2) for x in saiji_name]

    return saiji_name

def get_data(url):
    base_url = 'http://liansai.500.com'

    final_url = base_url + url

    response = requests.get(final_url).text

    content = etree.HTML(response)

    info = content.xpath('//*[@class="lcol_tit_r"]/a/@href')

    m = re.findall("jifen-[0-9]*",info[0])
    m = re.sub("\D", "", m[0])

    return int(m)


def get_list(id):
    saiji_list = []
    start_url = 'http://liansai.500.com/zuqiu-%s/' % id

    re = requests.get(start_url)
    content = etree.HTML(re.text)

    # for i in range(99,117):
    #     rule = '//*[@id="link%s"]/text()' % i
    #     detail = content.xpath(rule)
    #     print(len(detail))
    de = content.xpath('//*[@id="seaon_list_div"]/div[2]/div/ul/li[not(@class)]')
    for i in de:
        detail = i.xpath('a/@href')
        #print(detail)
        saiji = get_data(detail[0])
        saiji_list.append(saiji)

    return saiji_list

if __name__ == '__main__':
    id = input('Entering current season id: ')

    saiji_list = get_list(id)
    print(saiji_list)
    print(get_saiji_name1(saiji_list))
    print(get_saiji_name2(saiji_list))
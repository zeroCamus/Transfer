import requests
from bs4 import BeautifulSoup
import pymongo
import re

import time

MODE_FLOAT = re.compile(r'\d+.\d+')
MODE_INT = re.compile(r'\d+')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}




client = pymongo.MongoClient(host="127.0.0.1",port=27018)
db = client['MyAPP']


def store(data_list):
    for data in data_list:
        data_dict = {}
        if data[0] in name_set:
            continue
        name_set.add(data[0])
        data_dict['Name'] = data[0]
        data_dict['DownloadCount'] = data[1]
        data_dict['Category'] = data[2]
        col.insert_one(data_dict)

def get_ajax_data(union_id):
    request_url = "http://sj.qq.com/myapp/union/apps.htm?unionId=" + union_id
    raw_ajax_data = requests.get(request_url, headers=headers).json()
    ajax_data = raw_ajax_data['obj']
    return ajax_data

def get_soup(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def deal_count(str):
    try:
        count = float(MODE_FLOAT.findall(str)[0])
    except IndexError:
        count = float(MODE_INT.findall(str)[0])

    if '万' in str:
        count *= 10000
    elif '亿' in str:
        count *= 100000000
    return int(count)

def crawl(url):
  
    soup = get_soup(url)
    # print(soup)
    area = soup.find_all("li", {"class": "union-list  nopicshow J_Mod"})
    # if area == None:
    print(area)
    datas = []
    for part in area:
        sections = part.find_all("section", {"class": "union-list-app"})
        for section in sections:
            detail = section.find("div", {"class": "union-list-app-detail"})
            name = detail.find("a", {"class": "appName ofh"}).get_text()
            category_name = "none"
            raw_download = detail.find("span", {"class": "download"}).get_text()
            down_count = raw_download.replace("\r\t", "").replace("\r", "").replace(" ", "").replace("\n\t", "").replace("\n", "")
            count = deal_count(down_count)
            datas.append((name, count, category_name))
        info = part.find("div", {"class": "union-data-box"})
        idx = info.find("a").attrs['idx']
        ajax_data = get_ajax_data(idx)
        if ajax_data == None:
            continue
        for i in ajax_data:
            name = i['appName']
            down_count = i['appDownCount']
            category_name = i['categoryName']
            datas.append((name, down_count, category_name))
   
    store(datas)

def run():
    for i in range(1, 9):
        print(i)
        start_url = "http://sj.qq.com/myapp/union.htm?orgame=1&typeId=&page=" + str(i)
        crawl(start_url)

if __name__ == "__main__":
    while True:
        col_name = time.ctime().replace(" ", "_")
        col = db[col_name]
        name_set= set()
        run()
        time.sleep(60*60*12)
    

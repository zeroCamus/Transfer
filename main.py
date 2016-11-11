from bs4 import BeautifulSoup
from sendEmail import sendme

import requests
import lxml
import time


def crawl(url):
    try:
        html = requests.get(url)
    except:
        with open("log.log", "a") as file:
            file.write("Http error on " + time.ctime())
        time.sleep(60)
        return None
    soup = BeautifulSoup(html.text, 'lxml')
    data_list = []
    for cont in soup.find_all("div", {"class": "content"}):
        raw_data = cont.get_text()
        data = raw_data.replace("\n", "")
        data_list.append(data)
    return data_list


def sendToMe(data_list):
    email_text = ''
    for i in data_list:
        email_text += (i + "\n\n")
    try:
        sendme(time.ctime(), email_text)
    except:
        with open("log.log", "a") as file:
            file.write("Send email error on " + time.ctime())
    print("success", time.ctime())


def do():
    data_list = []
    for i in range(1, 6):
        url = 'http://www.qiushibaike.com/text/page/%s/' % str(i)
        temp_data = crawl(url)
        data_list.extend(temp_data)
    sendToMe(data_list)


def main():
    while True:
        do()
        time.sleep(43200)

main()

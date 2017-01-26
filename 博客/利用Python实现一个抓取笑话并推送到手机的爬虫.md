---
title: 利用Python实现一个抓取笑话并推送到手机的爬虫
date: 2017-01-26 21:30:40
categories: 技术
tags: Crawler
---
糗事百科（[http://www.qiushibaike.com/）](http://www.qiushibaike.com/%EF%BC%89) 是一个实时更新的笑话网站，会在主页实时显示出最新，最热门的笑话。我们在这里利用Python来制作一个定时抓取笑话，并推送到手机的爬虫，享受DIY的乐趣。
<!--more-->
## 需要额外安装的库

requests
`pip3 install requests`
BeautifulSoup
`pip3 install bs4`
lxml
`pip3 install lxml`

## 文件结构

- `sendEmail.py`：邮件发送模块，用在将消息推送到邮箱。
- `main.py`：主程序，负责抓取信息。

## 功能

每隔12小时就运行一次爬虫，爬虫将对糗事百科的前5页进行抓取，然后将抓取的内容打包，并推送到自己的手机。

## 使用方法

在自己的手机上装一个可接收实时推送的邮箱软件（如网易邮箱大师）。
将`sendEmail.py`内的收件箱和发件箱配置好。
将爬虫文件放在一个可以24小时开机的主机（推荐使用云服务器）上，运行`python3 main.py`。

## 代码

*sendEmail.py*

```
import smtplib
from email.mime.text import MIMEText

def sendme(title, text):
    msg = MIMEText(text)
    msg['Subject'] = title
    msg['From'] = "此处填入你用来发送邮件用的邮箱"
    msg['To'] = "此处填入你的接收端邮箱"
    s = smtplib.SMTP('smtp.126.com')
    s.login('此处填入发件箱用户名', '此处填入发件箱密码')
    s.send_message(msg)
    s.quit()

if __name__ == '__main__':
    sendme("Hello World", "Welcome")
```

*main.py*

```
from bs4 import BeautifulSoup
from sendEmail import sendme

import requests
import lxml
import time
def crawl(url):
    try:
        html = requests.get(url)
    except:
        with open("log.log","a") as file:
            file.write("Http error on " + time.ctime())
        time.sleep(60)
        return None
    soup = BeautifulSoup(html.text, 'lxml')
    data_list = []
    for cont in soup.find_all("div", {"class":"content"}):
        raw_data = cont.get_text()
        data = raw_data.replace("\n","")
        data_list.append(data)
    return data_list

def sendToMe(data_list):
    email_text  = ''
    for i in data_list:
        email_text += (i + "\n\n")
    try:
        sendme(time.ctime(), email_text)
    except:
        with open("log.log","a") as file:
            file.write("Send email error on " + time.ctime())
    print("success",time.ctime())

def do():
    data_list = []
    for i in range(1,6):
        url = 'http://www.qiushibaike.com/8hr/page/%s/?s=4906081'%str(i)
        temp_data = crawl(url)
        data_list.extend(temp_data)
    sendToMe(data_list)

def main():
    while True:
        do()
        time.sleep(43200)

main()
```
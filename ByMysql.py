from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import sendEmail
import pymysql
conn = pymysql.connect(host = '10.66.108.129',
                       user = 'root',passwd = 'xxttvv123',db = 'WikiDB')
cur = conn.cursor()

maxid = cur.execute("select max(id)  from pages")
flag = list(maxid)[0][0] + 1

def store(id, title, content):
    cur.execute("INSERT INTO pages (title, content) VALUES (?,?)", (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    global flag,links
    try:
          html = urlopen("http://en.wikipedia.org"+articleUrl)
    except:
        main()
    bsObj = BeautifulSoup(html, "lxml")
    try:
        title = bsObj.find("h1").get_text()
        content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    except:
        cur.execute("SELECT title FROM pages WHERE id=%d-3" % flag)
        urlTitle = cur.fetchall()[0][0]
        links = getLinks("/wiki/%s"%urlTitle)
        main()    
    store(title, content)
    flag += 1
    if(flag !=0 and flag%500 == 0):
        sendEmail.sendme("RESULT", "Crawler has scraped %d datas"%flag)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))



links = getLinks("/wiki/Middle")
def main():
    global links
    try:
        while len(links) > 0:
             newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
             print(newArticle)
             links = getLinks(newArticle)
    finally:
        cur.close()
        conn.close()
        sendEmail.sendme("RESULT", "程序挂掉了！")

if __name__ == '__main__':
    main()
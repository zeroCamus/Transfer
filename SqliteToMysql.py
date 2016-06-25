import pymysql
import sqlite3

mysqlConn = pymysql.connect(host = '10.66.108.129',
                       user = 'root',passwd = 'xxttvv123',db = 'WikiDB')
mysqlCur = mysqlConn.cursor()
print("Connect Success")
sqliteConn = sqlite3.connect("wikidata.db")
sqliteCur = sqliteConn.cursor()

sqliteCur.execute('''SELECT * FROM pages ''')
DataList = sqliteCur.fetchall()

for data in DataList:
    mysqlCur.execute('''INSERT INTO Pages (id, title, content) VALUES(?, ?, ?)''' % (data[0], data[1],data[2]))
    mysqlCu.connection.commit()

print("All Done")
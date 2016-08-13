Redis是一种基于内存的NoSQL数据库，我们利用它的特性，来实现一个实时聊天室。  
## 功能  
客户端要求能实时监控和接受消息，并且能向公共频道或者私人发送消息。要求能使用如下指令：  
* `pull`  拉取未读消息。  
* `users`  获得当前在线用户。  
* `pub <message>`  向大厅发送消息。  
* `to <someone>`  向某用户发送消息。  
* `downline`  下线。  

服务器端负责维护消息队列和存储消息记录。  
## 代码  
### 客户端  
```
import redis
import threading
import time
import queue


# 连接至Redis服务器，客户端需要配置主机IP和端口。
# 例如： conn = redis.Redis(host='xxx,xxx,xxx,xxx', port=6379, db=0)
conn = redis.Redis()

# 用户昵称
name = ''

# 消息记录缓冲池，每pull一次消息，就清空一次。
mes_queue = queue.Queue()

def _help():
    help_doc = '''pull 拉取消息\ndownline 下线\nusers 拉取当前在线用户\npub <message> 向大厅发布消息\nto <someone> 向某人发送消息'''
    print(help_doc)

def login():
    '''
    登陆，将昵称上传至服务器，保持登陆状态。
    '''
    global name, conn

    name = input("Please input your nickname(Blank is not allowed): ")
    if conn.sismember("users", name):
        print("The user already exists, please rename!")
        login()
    else:
        conn.sadd("users", name)
        print("Welcome! If you do not know the operating instructions, type \"help\" to get")


def orderAnalyse():
    '''
    词法分析，将user输入的命令分词并分析。
    '''
    global name, conn

    while True:
        message = input("Chatroom> ")
        order_list = message.lower().split(' ')

        if order_list[0] == 'pull':
            while not mes_queue.empty():
                print(mes_queue.get())
        elif order_list[0] == 'help':
            _help()
        elif order_list[0] == 'downline':
            conn.srem("users", name)
            print("Thank you")
            exit()
        elif order_list[0] == 'pub':
            mes_list = order_list[1:]
            message = ''
            for word in mes_list:
                message += (word + ' ')
            real_mes = name + ': ' + message
            conn.publish("chat", real_mes.encode("utf-8"))
        elif order_list[0] == 'to':
            if not conn.sismember("users", order_list[1]):
                print("This user does not exist")
                orderAnalyse()
            else:
                message = input(order_list[1] + "> ")
                real_mes = name + ': ' + message
                conn.publish(order_list[1], real_mes.encode("utf-8"))
        elif order_list[0] == 'users':
            users = conn.smembers("users")
            print(users)
        else:
            print("This command does not exist!")
            orderAnalyse()


def subPublic():
    '''
    负责监听公共频道。
    '''
    global mes_queue, conn

    sub = conn.pubsub()
    sub.subscribe(["chat"])
    for msg in sub.listen():
        if msg['data'] == 1:
            pass
        else:
            mes_queue.put(msg['data'].decode('utf-8'))


def subPrivate():
    '''
    负责监听私聊信息。
    '''
    global mes_queue, conn, name

    sub = conn.pubsub()
    sub.subscribe([name])
    for msg in sub.listen():
        if msg['data'] == 1:
            pass
        else:
            real_mes = '----------------------------------\n' +\
                       "whisper!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" +\
                       msg['data'].decode('utf-8') + '\n' +\
                       '----------------------------------'
            mes_queue.put(real_mes)


def run_client():
    '''
    程序入口，设置两个子线程，一个用来监听公共频道，另一个用来监听以自己命名的
    频道，主线程负责接收指令。
    '''
    login()

    subPub_thread = threading.Thread(target=subPublic)
    subPri_thread = threading.Thread(target=subPrivate)
    subPub_thread.setDaemon(True)
    subPub_thread.start()
    subPri_thread.setDaemon(True)
    subPri_thread.start()

    time.sleep(3)
    orderAnalyse()


if __name__ == '__main__':
    try:
        run_client()
    finally:
        if conn.sismember("users", name):
            conn.srem("users", name)
```
### 服务器端   
```
import redis
import sqlite3
import threading

# 服务器端。
conn = redis.Redis()


def pub():
    global conn
    while True:
        message = input("Please input message: ")
        real_mes = '\n----------------------------------\n' +\
                   'NOTEING!!!!!!!!!!!!!!!!!!!!!!!!!!!\n' +\
                   'Administrator say: ' + message + '\n' +\
                   '----------------------------------'
        conn.publish("chat", real_mes.encode("utf-8"))

def storeMesLog(raw_info):
    c = sqlite3.connect("meslog.db")
    cur = c.cursor()
    if 'Administrator say:' in raw_info:
        return 

    raw_info_list = raw_info.lower().split(':')
    name = raw_info_list[0].replace(" say", "")
    messsage = ''.join(raw_info_list[1:])
    cur.execute("CREATE TABLE IF NOT EXISTS " + name +\
     " (id INTEGER PRIMARY KEY AUTOINCREMENT, content text, CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")

    cur.execute("INSERT INTO " + name + " (content) VALUES (?)" , (messsage,))
    c.commit()

    cur.close()
    c.close()

def sub():
    global conn
    sub = conn.pubsub()
    sub.subscribe(["chat"])
    for msg in sub.listen():
        if msg['data'] == 1:
            pass
        else:
            storeMesLog(msg['data'].decode('utf-8'))

def run_server():
    sub_thread = threading.Thread(target=sub)
    sub_thread.setDaemon(True)
    sub_thread.start()
    pub()

if __name__ == '__main__':
    run_server()
```  
   
## 原理  
### 客户端
开始时输入昵称，并作为该用户的唯一标识，上传到Redis的`users set`，客户端可通过`users`命令拉取当前在线用户。主线程负责输入命令和发送消息。第一个子线程负责监听`chat`频道（公共频道），并将消息放入缓冲队列。第二个子线程负责监听名为自己昵称的频道，并将消息标记后入队。客户端可通过`pull`命令获取并刷新缓冲队列。  
### 服务器端  
子线程负责监听`chat`频道，并将消息分词，提取出昵称和消息内容，然后在数据库中寻找以该昵称为名的表（如果不存在将创建），并将消息存到该表中。主线程负责向`chat`频道发送消息。  
### 原理图  

![image](\img\Diagram.png)

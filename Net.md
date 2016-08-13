## 引言  
在日常的爬虫编写中，有些网站设置了权限，只有在登录了之后才能爬取网站的内容，导致常规的方法无法抓取。为了解决这个问题，目前的方法主要是利用浏览器cookie模拟登录。  
## 浏览器访问网页的过程  
在用户访问网页时，不论是通过URL输入域名或IP，还是点击链接，浏览器向WEB服务器发出了一个HTTP请求（Http Request），WEB服务器接收到客户端浏览器的请求之后，响应客户端的请求，发回相应的响应信息（Http Response），浏览器解析引擎，排版引擎分析返回的内容，呈现给用户。WEB应用程序在于服务器交互的过程中，HTTP请求和响应时发送的都是一个消息结构。   
![image](\img\headers.png)   
## 模拟登录的原理
当你要模拟登录一个网站时，首先要搞清楚网站的登录处理细节（发了什么样的数据，给谁发等...）。我是通过Chrome浏览器的开发者工具来抓取http数据包来分析该网站的登录流程。同时，我们还要分析抓到的post包的数据结构和header，要根据提交的数据结构和heander来构造自己的post数据和header。
分析结束后，我们要构造自己的HTTP数据包，并发送给指定url。我们通过requests模块提供的API来实现request请求的发送和相应的接收。  
## 具体实践  
现在我们以自己学校的教务处网站（笔者以山东农业大学为例，各大高校的登录的原理基本相同，大家可以用自己学校的网站或其他网站做实验）为例，分析如何进行模拟登录。  
### 分析网站结构  

![image](\img\jiaowu.png)  
如图，我们可以看到，要想成功登录，我们必须要正确的填写帐号、密码和验证码，然后点击登录按钮。  
### 正常登录和抓包  

我们先正确的填写上信息，然后按照常规的方式登录一遍（记得登陆前按F12打开chrome的网络监控选项，没有帐号的可以用自己学校教务处的网站实验）。  
登录进去后，我们在`Network`一栏可以看到如下网络活动。  
![image](\img\network.png)  
我们对所有的网络活动每个都点开看一下，看看有哪些数据交换活动，最后，我们把目光锁定在`loginAction.do`这个活动，因为我们在它的Form Data中发现了我们刚刚提交的数据。   
![image](\img\data.png)    

### 分析
我们刚刚输入的帐号密码验证码都包含在了```zjh,mm,v_yzm```三个字段中了。这说明，我们输入帐号密码的时候，构造了一个包含这三种信息的数据包发给了远程服务器，然后远程服务器进行认证，最后把反馈页面返回来，也就是登陆之后的教务处页面，现在我们就要自己伪造一个数据包，来模拟提交这三种数据，“骗取”服务器发回反馈。但是还有一个问题，就是帐号密码我们是事先知道的，那验证码呢？ 实际上，我们在进入教务处的登录入口时，就先进行了一次GET请求。所以我们要再分析一下登录页面。那么回到登录页面，我们继续抓取数据包，可以看到下列可以活动。  
![image](\img\yanzheng.png) 
这个活动的API地址是`http://202.194.133.59/validateCodeAction.do?` 我们点开它的`Rreview`可以看到它得到的是验证码。  
![image](\img\preview.png)  
所以我们可以断定，这个活动就是用来获取验证码的。  
### 理清思路  
那么，登录一次的全部流程我们已经知道了，下面我们来理清一下思路。首先，我们要先请求验证码API，获得验证码，然后在用验证码，帐号，密码伪造数据包，利用登录API，POST给远程服务器，服务器验证无误后，返回登陆成功后的页面，模拟登录成功。  

### 代码实现  
在这里我对山东农业大学的教务处进行了模拟登录，并用爬虫抓取了自己的课程表，下面分享一下我的代码。  
  
```
from PIL import Image

import requests
import json

# 抓包的到的验证码和登录API
checkcodeUrl = 'http://202.194.133.59/validateCodeAction.do'
pageUrl = 'http://202.194.133.59/loginAction.do'

# Cookies
s = requests.session()
captcha = s.get(checkcodeUrl, stream = True)

# 保存验证码
with open("cap.gif", "wb") as file:
    for line in captcha.iter_content(10):
        file.write(line)

# 打开验证码，并要求输入
img = Image.open("cap.gif")
img.show()

num = input("请输入验证码:")
name = input("请输入学号:")
password = input("请输入教务处密码:")

# 构造请求头，伪装爬虫
headers_base = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}
user_data = {"zjh":name, "mm":password, "v_yzm":num}

s.post(pageUrl, headers = headers_base, data = user_data)

# 课程表API
scheduleUrl = 'http://202.194.133.59/xkAction.do?actionType=6'
schedule = s.get(scheduleUrl)
with open("schedule.html", "w") as f:
    f.write(schedule.text)

print("课表已成功下载到该文件夹下！")
```  

## 结语   
该实践只是演示了最简单的模拟登录方式，某些网站（如淘宝）采用了密码加密技术，POST过去的是被加密后的密码，对于这些网站，我们就要具体问题具体分析，找出它的加密方式，然后伪造出加密数据包，从而实现登录。  

这个网站的大部分内容都是利用的Ajax异步请求，AJAX可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新，也就告诉我们，如果我们从网站的源代码着手分析，是找不出这些活动的链接的，因为它们是在后期动态加载的。所以对于这种网站，我们要利用好浏览器的开发者工具，对其进行动态分析，抓出它相应活动的API，从而进行爬虫活动。有关Ajax方面的抓取技术，最近会写一篇博客专门介绍。  


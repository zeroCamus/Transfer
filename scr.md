豆瓣电影是豆瓣网推出的一个电影评价网站，网民可以对任意一部电影进行评价和打分，打分的分值在0-10之间，分数越高代表网民对该电影的认可度越高，而豆瓣电影TOP250（https://movie.douban.com/top250）是豆瓣电影的一个分值，该网站会实时显示出电影评分在前250的电影信息。我们将利用Scrapy框架对该网站进行抓取。  
<!--more-->  
## 需要额外安装的库  
scrapy(scrapy已经加入了对Python3的支持)  
`pip3 install scrapy`  
## 代码编写
**********  
### 启动项目
我们先开始一个Scrapy项目。  
`$ scrapy startproject DouBan`   
这时，项目文件夹下会出现如下结构。
```
│  scrapy.cfg
│
└─DouBan
    │  items.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    ├─spiders
    │  │  __init__.py
    │  │
    │  └─__pycache__         
    │
    └─__pycache__  
```   
这些文件分别是:  
* `scrapy.cfg`: 项目的配置文件。  
* `DouBan/`: 该项目的python模块。之后您将在此加入代码。  
* `DouBan/items.py`: 项目中的item文件。  
* `DouBan/pipelines.py`: 项目中的pipelines文件。  
* `DouBan/settings.py`: 项目的设置文件。  
* `DouBan/spiders/`: 放置spider代码的目录。  
### Item  
`Item` 是保存爬取到的数据的容器；其使用方法和`python字典`类似， 并且提供了额外保护机制来避免拼写错误导致的未定义字段错误。

您可以通过创建一个 `scrapy.Item` 类， 并且定义类型为 `scrapy.Field` 的类属性来定义一个`Item`。 

首先根据需要从豆瓣获取到的数据对`item`进行建模。 我们需要从`spider`中获取电影名字，评分，以及该电影的描述。 对此，在item中定义相应的字段。编辑 DouBan 目录中的 items.py 文件:    
```
import scrapy

class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    info = scrapy.Field()
    star = scrapy.Field()
    evaNum = scrapy.Field()
    quote = scrapy.Field()

```  
### Spider  
编写爬虫(Spider)
`Spider`是用户编写用于从单个网站(或者一些网站)爬取数据的类。

其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 `item` 的方法。

为了创建一个`Spider`，您必须继承 `scrapy.Spider` 类（对于更高级的爬虫，要继承`scrapy.CrawlSpider`类）， 且定义以下三个属性:

`name`: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。  
`start_urls`: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。  
`parse()` :`parse()`是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。  
以下为我们的一个`Spider`代码，保存在 `DouBan/spiders` 目录下的 `douban.py` 文件中:
```
from DouBan.items import DoubanItem
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

class DouBanSpider(CrawlSpider):
    name = 'doubanSpider'
    start_urls = [
    'http://movie.douban.com/top250',
    ]
    
    t_url = 'http://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanItem()
        sel = Selector(response)

        movie_infos = sel.xpath('//div[@class="info"]')
        for movie_info in movie_infos:
            title = movie_info.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            # 电影介绍内有许多无关字符，所以需要清理一下
            t_info = movie_info.xpath('div[@class="bd"]/p/text()').extract()
            t1_info = t_info[0].replace("\n", '')
            info = t1_info.replace(" ", '')
            star = movie_info.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            evaNum = movie_info.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()').extract()
            quote = movie_info.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

            item['title'] = title
            item['info'] = info
            item['star'] = star
            item['evaNum'] = evaNum
            item['quote'] = quote

            yield item

        url = sel.xpath('//span[@class="next"]/link/@href').extract()
        if url:
            url = url[0]
            print(url)
            yield Request(self.t_url + url, callback=self.parse)

```   

### Item Pipeline
当`Item`在`Spider`中被收集之后，它将会被传递到`Item Pipeline`，一些组件会按照一定的顺序执行对`Item`的处理。

每个`item pipeline`组件是实现了简单方法的Python类。他们接收到`Item`并通过它执行一些行为，同时也决定此`Item`是否继续通过`pipeline`，或是被丢弃而不再进行处理。

以下是`item pipeline`的一些典型应用：

* 清理HTML数据  
* 验证爬取的数据(检查item包含某些字段)  
* 查重(并丢弃)  
* 将爬取结果保存到数据库中   


我们编写一个自己的`Pipeline`，用来将抓取的内容存入到`MongoDB`中，在`Douban/pipelines.py`中写入如下内容：  
```
from pymongo import MongoClient
from scrapy.conf import settings

class DoubanPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        name = settings['MONGODB_DBNAME']
        client = MongoClient(host=host,port=port)
        db = client[name]
        self.col = db[settings['MONGODB_DOCNAME']]
    def process_item(self, item, spider):
        movieInfo = dict(item)
        self.col.insert(movieInfo)
        return item

```  
以上代码可以将抓取的内容已键值对的形式保存到`MongoDB`中。  
### settings
为了启用`Pipeline`组件，你必须将它的类添加到 `ITEM_PIPELINES` 配置，在`DouBan/setting.py`中写入：  
```
ITEM_PIPELINES = {
    'DouBan.pipelines.DoubanPipeline': 1,
}

```   
同时，还要把`MongoDB`的对应参数写入`DouBan/setting.py`中：  
```
ROBOTSTXT_OBEY = True
COOKIES_ENABLED = True
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'DouBan'
MONGODB_DOCNAME = 'Movies'
```
##  运行  
将文件夹定位到项目目录，输入  
`scrapy crawl doubanSpider`   
爬虫就会开始运行，等待程序运行完之后，打开MongoDB，就能看到被抓下来的电影信息了。   
   
     

*********
查看完整代码请[点击此处](https://github.com/WiseDoge/DouBan_Spider)(https://github.com/WiseDoge/DouBan_Spider)  
本文参考于scrapy官方文档，查看完整Scrapy官方文档请[点击此处](http://doc.scrapy.org/en/latest/index.html)
            
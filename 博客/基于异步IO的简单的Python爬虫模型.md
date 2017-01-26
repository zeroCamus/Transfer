---
title: 基于异步IO的简单的Python爬虫模型
date: 2017-01-26 21:30:18
categories: 技术
tags: Crawler
---
我们利用`asynico`框架来实现一个简单的异步抓取爬虫，该爬虫可以对一个一组给定的URL进行异步抓取，并返回网页的源代码。
<!--more-->
## 什么是异步IO

CPU的速度远远快于磁盘、网络等IO。在一个线程中，CPU执行代码的速度极快，然而，一旦遇到IO操作，如读写文件、发送网络数据时，就需要等待IO操作完成，才能继续进行下一步操作。这种情况称为同步IO。

在IO操作的过程中，当前线程被挂起，而其他需要CPU执行的代码就无法被当前线程执行了。此状态下，虽然CPU的运算能力富余，但是上一个IO操作没有完成，之后的代码也无法执行。我们要想一种办法解决这种问题，有人提出可以用多线程+多进程的并发方案，将任务分配到多个线程上，虽然当前线程被挂起，但是其他的线程可以不受影响。但是，系统的线程和进程不能无上限的增加，由于系统切换线程的开销也很大，所以，一旦线程数量过多，CPU的时间就花在线程切换上了，真正运行代码的时间就少了，结果导致性能严重下降。

所以又有人提出了异步IO的思想，当代码需要执行一个耗时的IO操作时，它只发出IO指令，并不等待IO结果，然后就去执行其他代码了。一段时间后，当IO返回结果时，再通知CPU进行处理。这样就可以在一个线程上实现类似于“多线程”的代码。

## asyncio是什么

先来看看官方的介绍

> This module provides infrastructure for writing single-threaded concurrent
> code using coroutines, multiplexing I/O access over sockets and other resources,
> running network clients and servers, and other related primitives.

`asyncio`是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。

`asyncio`的编程模型就是一个消息循环。我们从`asyncio`模块中直接获取一个`EventLoop`的引用，然后把需要执行的协程扔到`EventLoop`中执行，就实现了异步IO。

在Python3.5中，引入了两个新的关键字`async`和`await` 代替了原来的`@asyncio.coroutine` 和`yield from`,这就大大的简化了代码结构。

除此之外，我们还需要`aiohttp`，这个库是一个第三方网络库，可以很好的于`asyncio`结合，达到异步下载的目的。

## 需要安装的库

asyncio

`pip install asyncio`

aiohttp

`pip install aiohttp`

## 代码实现

```
import asyncio
import aiohttp


class Downloader(object):

    def __init__(self, urls):
        self.urls = urls
        self.__htmls = []
        
    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self.__htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))
	@property
    def get_htmls(self):
        return self.__htmls


if __name__ == '__main__':
    urls = ['http://wisedoge.top',
            'http://wisedoge.top']
    d = Downloader(urls)
    d.download()
    print(d.htmls)
```
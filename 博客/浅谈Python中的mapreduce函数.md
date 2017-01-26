---
title: 浅谈Python中的map reduce函数
date: 2017-01-28 21:30:27
categories: 技术
tags: Python
---
如果你对Google的MapReduce有所了解的话，那你大概会明白map/reduce的概念。在本文中，我整理了一下python中map、reduce、filter等函数的用法。
<!--more-->
### map

map函数接受两个参数，一个是操作函数(func)，一个是可迭代对象(iter)，返回一个新的迭代器。

map的作用是对iter中的每一个元素都使用func，并将结果作为一个迭代器返回。

来看看具体的用法

```
r = map(lambda x: x**2, range(10))
print(list(r))
```

结果

```
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

再来一个例子，现在给定一份姓名的名单，要求我们把每个名字的首字母变成大写，我们用map实现如下

```
names = ['liu', 'zhang', 'li', 'wang', 'lin', 'wu']
cor_names = map(lambda x: x[0].upper() + x[1:], names)
print(list(cor_names))
```

结果

```
['Liu', 'Zhang', 'Li', 'Wang', 'Lin', 'Wu']
```

### reduce

`reduce`把一个函数作用在一个序列`[x1, x2, x3, ...]`上，这个函数必须接收两个参数，`reduce`把结果继续和序列的下一个元素做累积计算，其效果就是：

```
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
```

我们来编写一个将列表中所有元素求和的例子

```
from functools import reduce
r = reduce(lambda x,y: x + y, list(range(10)))
print(r)
```

运行结果

```
45
```

### filter

Python内建的`filter()`函数用于过滤序列。和`map()`类似，`filter()`也接收一个函数和一个序列。和`map()`不同的是，`filter()`把传入的函数依次作用于每个元素，然后根据返回值是`True`还是`False`决定保留还是丢弃该元素。

我们来完成一个例子，找出一个列表中的奇数

```
nums = filter(lambda x: x%2, range(10))
print(list(nums))
```

运行结果

```
[1, 3, 5, 7, 9]
```
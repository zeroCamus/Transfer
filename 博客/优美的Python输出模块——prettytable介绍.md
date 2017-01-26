---
title: 优美的Python输出模块——prettytable介绍
date: 2017-01-26 21:30:15
categories: 技术
tags: Python
---
许多用过MySQL的同学可能知道，MySQL的命令行表格输出是非常优美的(如下图)，其实这个功能可以利用Python的prettytable模块达到，这次我们来介绍一下这个库的使用方式。
<!--more-->
![image](pic\youmei1.png)

## 安装

`pip3 install prettytable`

## 使用

- 引入prettytable包

  `from prettytable import PrettyTable`

- 创建PrettyTable对象

  每一个输出表格就是一个PrettyTable对象，首先我们需要实例化一个表格对象，我们需要传一个列表作为构造函数的参数，这个列表里包含了表格的所有字段。

  `row = PrettyTable(["Name", "Sex", "Grades"])`

- 向表格中添加数据

  使用`add_row`方法，将一条记录以列表的形式添加

  `row.add_row(["Liu", "man", 100])`

  `row.add_row(["Zhang", "woan", 10])`

- 打印表格

  直接调用`print`函数即可

  `print(row)`

![image](pic\youmei2.png)
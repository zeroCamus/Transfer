---
title: Python运算符重载举例
date: 2017-01-28 21:30:22
categories: 技术
tags: Python
---
我们利用Python的运算符重载，来实现一个加强版的List。
<!--more-->
## 运算符重载

运算符重载，就是对已有的运算符重新进行定义，赋予其另一种功能，以适应不同的数据类型。

先来看看常见的可重载的运算符

| method                                   | overload  | call                                     |
| ---------------------------------------- | --------- | ---------------------------------------- |
| __init__                                 | 构造函数      | 对象创建: X = Class(args)                    |
| __del__                                  | 析构函数      | X对象收回                                    |
| __add__                                  | 云算法+      | 如果没有*iadd*， X+Y， X+=Y                    |
| __or__                                   | 运算符 或     | 提供or的功能                                  |
| __repr__, __str__                        | 打印，转换     | print(X)，repr(X)，str(X)                  |
| __call__                                 | 函数调用      | X(*args, \**kwargs)                      |
| __getattr__                              | 点号运算      | X.undefined                              |
| __setattr__                              | 属性赋值语句    | X.any=value                              |
| __delattr__                              | 属性删除      | del X.any                                |
| __getattribute__                         | 属性获取      | X.any                                    |
| __getitem__                              | 索引运算      | X[key]，X[i:j]                            |
| __setitem__                              | 索引赋值语句    | X[key]，X[i:j]=sequence                   |
| __delitem__                              | 索引和分片删除   | del X[key]，del X[i:j]                    |
| __len__                                  | 长度        | len(X)，如果没有__bool__，真值测试                 |
| __bool__                                 | 布尔测试      | bool(X)                                  |
| __lt__, __gt__, __le__, __ge__, __eq__, __ne__ | 特定的比较     | XY，X<=Y，X>=Y， X==Y，X!=Y 注释：（lt: less than, gt: greater than, le: less equal, ge: greater equal, eq: equal, ne: not equal ） |
| __radd__                                 | 右侧加法      | other+X                                  |
| __iadd__                                 | 实地（增强的）加法 | X+=Y(or else __add__)                    |
| __iter__, __next__                       | 迭代环境      | I=iter(X), next()                        |
| __contains__                             | 成员关系测试    | item in X(任何可迭代)                         |
| __index__                                | 整数值       | hex(X), bin(X), oct(X)                   |
| __enter__, __exit__                      | 环境管理器     | with obj as var:                         |
| __get__, __set__, __delete__             | 描述符属性     | X.attr, X.attr=value, del X.attr         |
| __new__                                  | 创建        | 在__init__之前创建对象                          |

我们基于这个表格，来写个小例子，加深一下理解。

## 例子

### 代码

```
class MyList(object):

    def __init__(self, value):
        # 由列表创建对象
        self._val = value.copy()

    def __add__(self, other):
        ans = []
        if isinstance(other, (int, float)):
            for i in self._val:
                ans.append(i + other)
        else:
            for x, y in zip(self._val, other._val):
                ans.append(x + y)
        return MyList(ans)
    
    def __iadd__(self, other):
        if isinstance(other, (int, float)):
            for i in range(len(self._val)):
                self._val[i] += other
        else:
            for i in range(len(self._val)):
                self._val[i] += other._val[i]
        return self

    def __call__(self, i):
        return self._val[i]

    def __sub__(self, other):
        ans = []
        if isinstance(other, (int, float)):
            for i in self._val:
                ans.append(i - other)
        else:
            for x, y in zip(self._val, other._val):
                ans.append(x - y)
        return MyList(ans)
    
    def __eq__(self, other):
        if len(self._val) != len(other._val):
                return False
        for x, y in zip(self._val, other._val):
            if x != y:
                return False
        return True

    def __getattr__(self, attrname):
        if attrname == 'length':
            return len(self)
    
    def __iter__(self):
        for i in self._val:
            yield i

    def __getitem__(self, i):
        if isinstance(i, int):
            return self._val[i]
        if isinstance(i, slice):
            return self._val[i.start:i.stop:i.step]

    def __contains__(self, other):
        return True if other in self._val else False

    def __setitem__(self, i, value):
        self._val[i] = value

    def __repr__(self):
        return repr('MyList({})'.format(self._val))

    def __str__(self):
        return str(self._val)

    def __len__(self):
        return len(self._val)
```

我们再编写一个测试，测试一下。

### 测试

```
class MyListTest(unittest.TestCase):

    def setUp(self):
        self.l = MyList([1, 2, 3])

    def test_get(self):
        self.assertEqual(self.l[1], 2)

    def test_in(self):
        self.assertTrue(1 in self.l)
        self.assertFalse(5 in self.l)

    def test_len(self):
        self.assertEqual(len(self.l), 3)

    def test_get_attr(self):
        self.assertEqual(self.l.length, 3)

    def test_set(self):
        self.l[1] = 100
        self.assertEqual(self.l[1], 100)

    def test_add(self):
        l2 = MyList([2, 3, 4])
        l3 = self.l + 1 
        self.assertEqual(l3, l2)
        self.assertEqual(l2+l2, MyList([4, 6, 8]))

    def test_sub(self):
        l2 = MyList([2, 3, 4])
        l3 = l2 - 1
        self.assertEqual(l3, self.l)
        self.assertEqual(l2 - self.l, MyList([1, 1, 1]))

    def test_iadd(self):
        l2 = MyList([2, 3, 4])
        self.l += 1
        self.assertEqual(self.l, l2)
        l2 += l2
        self.assertEqual(MyList([4, 6, 8]), l2)

    def test_iter(self):
        flag = 1
        for i in self.l:
            self.assertEqual(i, flag)
            flag += 1 
        flag = 1
        self.assertFalse(3 in self.l[:2])

    def test_eq(self):
        l2 = MyList([1, 2, 3])
        self.assertEqual(self.l, l2)

    def test_call(self):
        self.assertEqual(self.l(1), 2)
```

### 测试运行结果

```
...........
----------------------------------------------------------------------
Ran 11 tests in 0.063s

OK
```
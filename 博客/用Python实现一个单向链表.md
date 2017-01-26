---
title: 用Python实现一个单向链表
date: 2017-01-28 21:30:29
categories: 技术
tags: Python
---
我们用Python来实现一个具有中间插入，尾部插入，删除，求长度，打印，搜索，合并等功能的单项链表。
<!--more-->
### 编写节点

```
class Node(object):
    '''节点类
    '''
    __slots__ = ('_value', '_next')
    
    def __init__(self, value):
        self._value = value
        self._next = None
```

### 编写链表类

```
class List(object):
    
    def __init__(self):
        self._root = None
        
    def is_empty(self):
        '''判断链表是否为空，如果为空，返回True，否则返回False
        '''
        return True if self._root == None else False
            
    def push_back(self, value):
        '''在链表尾部插入value
        '''
        if self.is_empty():
            self._root = Node(value)
        else:
            node_ptr = self._root
            while node_ptr._next != None:
                node_ptr = node_ptr._next
            node_ptr._next = Node(value)
    
    def insert(self, key, value):
        '''在给定key的前面插入value，如果找不到给key则不作插入
        '''
        node_ptr = self._root
        pre_ptr = None
        while node_ptr._value != key:
            pre_ptr = node_ptr
            node_ptr = node_ptr._next
            if not node_ptr:
                return 
        if pre_ptr:
            pre_ptr._next = Node(value)
            pre_ptr._next._next = node_ptr
        else:
            self._root = Node(value)
            self._root._next = node_ptr

    def length(self):
        '''长度
        '''
        if self.is_empty():
            return 0
        count = 1
        node_ptr = self._root
        while node_ptr._next != None:
            count += 1
            node_ptr = node_ptr._next
        return count
        
        
    def merge(self, other):
        '''将other合并到self
        '''
        node_ptr = self._root
        while node_ptr._next != None:
            node_ptr = node_ptr._next
        node_ptr._next = other._root
    
    def remove(self, value):
        '''删除给定value，如果不存在则不做处理
        '''
        node_ptr = self._root
        pre_ptr = None
        while node_ptr:
            if node_ptr._value == value:
                if not pre_ptr:
                    self._root = node_ptr._next
                else:
                    pre_ptr._next = node_ptr._next
                break
            else:
                pre_ptr = node_ptr
                node_ptr = node_ptr._next
    
    def search(self, value):
        '''搜索，如果value在链表内，返回True，否则返回False
        '''
        if self.is_empty():
            return False
        node_ptr = self._root
        while True:
            if node_ptr._value == value:
                return True
            if node_ptr._next == None:
                return False
            node_ptr = node_ptr._next
    
    def __iter__(self):
        node_ptr = self._root
        while True:
            yield node_ptr._value
            if node_ptr._next == None:
                break
            node_ptr = node_ptr._next

    def __repr__(self):
        ans = []
        if self.is_empty():
            return repr(ans)
        node_ptr = self._root
        while True:
            ans.append(node_ptr._value)
            if node_ptr._next == None:
                break
            node_ptr = node_ptr._next
        return repr(ans)
```

`__repr__`方法是为了打印链表，`__iter__`方法是为了迭代。

### 写一个简单的测试

```
class LinkListTest(unittest.TestCase):

    def setUp(self):
        self.l = List()

    def test_is_empty(self):
        self.assertTrue(self.l.is_empty())

    def test_length(self):
        self.assertEqual(self.l.length(), 0)
        self.l.push_back(1)
        self.assertEqual(self.l.length(), 1)
        self.l.push_back(2)
        self.l.push_back(3)
        self.l.push_back(4)
        self.assertEqual(self.l.length(), 4)

    def test_search(self):
        self.l.push_back(1)
        self.l.push_back(2)
        self.assertTrue(self.l.search(1)) 
        self.assertTrue(self.l.search(2))
        self.assertFalse(self.l.search(3))
    
    def test_remove(self):
        self.l.push_back(1)
        self.l.push_back(2)
        self.l.push_back(3)
        self.l.push_back(4)
        self.l.remove(1)
        self.assertFalse(self.l.search(1))
        self.l.remove(4)
        self.assertFalse(self.l.search(4))
        self.l.remove(2)
        self.assertFalse(self.l.search(2))

    def test_iter(self):
        self.l.push_back(1)
        self.l.push_back(2)
        self.l.push_back(3)
        self.l.push_back(4)
        count = 1
        for i in self.l:
            self.assertEqual(i, count)
            count += 1

    def test_merge(self):
        l2 = List()
        l2.push_back(3)
        l2.push_back(4)
        self.l.push_back(1)
        self.l.push_back(2)
        self.l.merge(l2)
        count = 1
        for i in self.l:
            self.assertEqual(i, count)
            count += 1

    def test_insert(self):
        self.l.push_back(2)
        self.l.push_back(4)
        self.l.push_back(6)
        self.l.insert(2, 1)
        self.l.insert(4, 3)
        self.l.insert(6, 5)
        count = 1
        for i in self.l:
            self.assertEqual(i, count)
            count += 1
        self.l.insert(33, 100)
        self.assertFalse(self.l.search(100))
```

### 测试运行结果

```
.......
----------------------------------------------------------------------
Ran 7 tests in 0.031s

OK
```
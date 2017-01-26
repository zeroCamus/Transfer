---
title: 用C来加速你的Python程序
date: 2017-01-28 21:30:28
categories: 技术
tags: Python
---
众所周知Python在做多重循环运算时的速度非常慢，通常为了加速Python可以选择在Python中嵌入C/C++的动态链接库，我们这次探讨一下C嵌入Python的优点。
<!--more-->
## 性能测试

测试对象是一个名为fortest的函数，我们先来看看它的Python实现

```
def fortest(x):
    root = 0
    for i in range(x):
        for j in range(x):
            for k in range(x):
                root += (i+j+k)
    for i in range(x):
        for j in range(x):
            for k in range(x):
                root += (i+j+k)
    return root
```

再来看看它的C实现

```
long long fortest(int x)
{
	long long root = 0;
	for (int i = 0; i < x; ++i) 
		for (int j = 0; j < x; ++j) 
			for (int k = 0; k < x; ++k) 
				root += (i + j + k);
	for (int i = 0; i < x; ++i) 
		for (int j = 0; j < x; ++j) 
			for (int k = 0; k < x; ++k) 
				root += (i + j + k);					
	return root;
}
```

编写测试

```
import ctypes
from time import time

dll = ctypes.windll.LoadLibrary("stest.dll")

def fortest(x):
    root = 0
    for i in range(x):
        for j in range(x):
            for k in range(x):
                root += (i+j+k)
    for i in range(x):
        for j in range(x):
            for k in range(x):
                root += (i+j+k)
    return root

start = time()
print(fortest(160))
end = time()

print(end-start)

start = time()
print(dll.fortest(160))
end = time()

print(end-start)
```

速度对比（三组数据）

```
1953792000
0.750096321105957
1953792000
0.015610694885253906
```

```
1953792000
0.7501065731048584
1953792000
0.015630722045898438
```

```
1953792000
0.6875753402709961
1953792000
0.01563262939453125
```

可以看出，C实现比Python实现快了70倍之多，所以在日常的使用中，如果的程序从算法的角度已经优化到极限，可是速度仍然达不到要求，可以考虑使用ctpyes模块提供的C类型或者直接调用C模块来提速。

## 多线程测试

C的链接库可以打破Python多线程运行在单核上的限制，实现真正的多线程，可看如下例子(在四核心电脑上运行)。

```
#include "stdafx.h"
#include "sci.h"


SCI_API int prime(int n)
{
	int count = 0;
	for (int i = 3; i <= n; ++i)
	{
		for (int j = 2; j < i; ++j)
		{
			if (i%j == 0)
			{
				++count;
				break;
			}

		}
	}
	return count;
}
```

```
#ifdef SCI_EXPORTS
#define SCI_API __declspec(dllexport)
#else
#define SCI_API __declspec(dllimport)
#endif


extern "C"{
	SCI_API int prime(int n);
}
```

将上述代码编译成动态链接库，然后导入Python。

```
import ctypes
import threading
import time
import queue

queue = queue.Queue()

dll = ctypes.windll.LoadLibrary("sci.dll")

ARG = 30000


def prime_c(x):
    count = dll.prime(x)
    queue.put(count)


def prime_py(x):
    count = 0
    for i in range(3, x + 1):
        for j in range(2, i):
            if i % j == 0:
                count += 1
                break
    queue.put(count)

start = time.time()
prime_py(ARG)
node_1 = time.time()
print("Single thread by python")
print(node_1 - start)

py_threads = []

for i in range(4):
    thread = threading.Thread(target=prime_py, args=(ARG,))
    thread.start()
    py_threads.append(thread)


for thread in py_threads:
    thread.join()

node_2 = time.time()
print("Multithreading  by python")
print(node_2 - node_1)

node_3 = time.time()
prime_c(ARG)
node_4 = time.time()
print("Single thread by C")
print(node_4 - node_3)

c_threads = []

for i in range(4):
    thread = threading.Thread(target=prime_c, args=(ARG,))
    thread.start()
    c_threads.append(thread)


for thread in c_threads:
    thread.join()


print("Multithreading thread by C")
node_5 = time.time()
print(node_5 - node_4)
```

运行结果

```
Single thread by python
5.078523874282837
Multithreading  by python
33.37398290634155
Single thread by C
0.1303727626800537
Multithreading thread by C
0.16142940521240234
```

在Python中，为了解决多线程之间数据完整性和状态同步，使用了全局解释器锁（GIL，Global Interpreter Lock），毫无疑问全局锁的存在会对多线程的效率有不小影响。用Python写的函数并没有将计算任务分布到四个核心上，而是由一个CPU核心轮番执行，而用调用了用C实现的函数，就可以实现真正的Python多线程。
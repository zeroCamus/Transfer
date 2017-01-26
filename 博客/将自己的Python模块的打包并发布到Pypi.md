---
title: 将自己的Python模块的打包并发布到Pypi
date: 2017-01-26 21:30:19
categories: 技术
tags: Python
---
通常，当我们制作了一个Python模块之后，要想在其他项目中使用，我们可以把该模块复制到其他项目的目录中，然后再`import`来使用。但是，如果我们有许多个项目都要使用这个模块，岂不是要将它复制很多份了？为了解决这个问题，我们可以将模块打包，然后加入到系统环境变量里，这样就可以直接在项目中`import`了。那如果，我们希望将自己的包分享给网络上的其他用户使用，该怎么做呢？方法有很多，比如用百度云，发邮件，发QQ附件等等……。但是最优雅和最Pythonic的方法是将包发布到Pypi，其他用户只需`pip install +包名`就可以安装并使用了。下面我们将介绍如何将模块的打包和发布到Pypi。
<!--more-->
## 将模块打包

模块打包，我们需要用到的第三方模块是setuptools，我们可以通过pip来安装:

`pip install setuptools`

安装好setuptools后，我们建立一个项目文件夹demo（正式的生产环境中，项目文件夹和内层的包文件夹要用同样的名字）。然后我们将自己的包放入到这个文件夹内，然后，我们在这个文件夹下放入包的README，开源协议，其他需要的外部文件。以及再新建一个名为setup.py的空的Python文件，到现在为止，demo文件夹的目录树如下（zquery文件夹就是要打包的模块）：

```
demo
 │  LICENSE
 │  README.md
 │  run.py
 │  setup.py
 │
 └─zquery
```

然后我们开始编写安装文件，将下面这个模版拷贝到setup.py内，在根据自己的实际情况更改一下即可。

```
from setuptools import setup

setup(
    name='name of the package',
    version='your version',
    description='your description',
    long_description = 'your long description',
    author='your name',
    author_email='your email',
    url='the package`s url',
    packages=[
        'name of the package'
    ],
    # py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        # install_requires
    ],
    # entry_points={
    #     'console_scripts': ['zquery=run:cli']
    # },
    license='apache 2.0',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
```

这样，一个可安装的Python包就制作好了，我们只需要执行 `python setup.py install` 就可以将该包安装了。

## 将模块发布到Pypi

首先要到Pypi的官网[https://pypi.python.org/pypi，点击右侧的Register注册一个Pypi帐号。](https://pypi.python.org/pypi%EF%BC%8C%E7%82%B9%E5%87%BB%E5%8F%B3%E4%BE%A7%E7%9A%84Register%E6%B3%A8%E5%86%8C%E4%B8%80%E4%B8%AAPypi%E5%B8%90%E5%8F%B7%E3%80%82)

然后我们在回到项目文件夹，运行 `python setup.py sdist`

这时，项目文件夹下会生成一个名为dist的文件夹，这个文件夹内保存的就是一个已经压缩好了的，并且可以上传到Pypi上的包了。同时还会产生一个名为 `包名.egg-info` 的文件夹，这里面包含的就是一些包的基本信息。

这些都准备好了之后，我们就可以准备上传了，我们运行`python setup.py register sdist upload`，然后按照提示就可以上传了，需要注意的是，第一次使用该命令时，会要求你输入刚刚注册的帐号和密码，输入完之后，系统会在本地存有一个记录文件，记录着你的帐号密码，以后再上传的时候，就无需再次输入帐号密码了。

文件上传好了之后，等待大概一个小时左右，互联网上的其他用户就可以通过 `pip install +包名` 来安装你的包了。
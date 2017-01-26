---
title: Spring学习笔记之八——Spring Expression Language
date: 2017-01-27 21:30:27
categories: 技术
tags: Java
---
Spring3时代引入了Spring表达式语言（Spring Expression Language），它能够以一种强大和简洁的方式将值装配到bean属性和构造参数中，在这个过程中所使用的表达式会在运行时计算得到值。使用SpringEL，你可以实现超乎想象的装配效果，这是其他装配技术所达不到的。
<!--more-->
## Spring EL的特性

- 使用Bean的ID来引用Bean
- 调用方法和访问对象的属性
- 对值进行算数，关系和逻辑运算
- 正则表达式匹配
- 集合操作

以下是Spring的几种常用运算符

| 运算符类型 | 运算符                                   |
| ----- | ------------------------------------- |
| 算数运算  | +, -, *, /, %, ^                      |
| 比较运算  | <, >, == ,<=, >=, eq, lt, get, le, ge |
| 逻辑运算  | and, or, not                          |
| 条件运算  | ?:(Ternary), ?:(Elvis)                |
| 正则表达式 | matches +                             |
| 集合    | []                                    |
| 查询运算  | ?.[] .^[] .$[]                        |
| 投影运算  | !.[]                                  |

## Spring EL的格式

### 书写格式

SpEL表达式要放到“#{ … }”之中。比如说下面就是一个最简单的SpEL

```
#{1}
```

该式的值为数字1，当然，Spring使用常量并没有什么意义。 下面这个式子会使SpEL更有意思。

### 使用T()运算符

```
#{T(java.lang.Math).random()}
```

在SpEL中，要想使用类的作用域的静态方法和常量时，可以用T()运算符来实现，在这里调用数学类的方法生成一个0到1之间的随机数。

### 使用Bean

如果想使用Bean的属性，可以使用下面的式子

```
#{father.name}   /    #{father.getName()}
```

这代表使用名为fahter的Bean的name属性。

我们也可以对这个属性再调用其他方法来加工

```
#{father.getName().toUpperCase()}    转换为大写 [1]
```

但为了保证getName()的值不为空，可以使用安全运算符?.

```
#{father.getName()?.toUpperCase()}  [2]
```

当getName()的值不为null时，安全运算符并没有表现出什么，但是如果该值为null时，[1]式会对null值调用toUpperCase()方法，会抛出异常，而[2]式会直接返回null。

对于上述运算符，这里有一个绝佳的例子将他们结合起来，请看下式

```
#{2 * T(java.lang.Math).PI * circle.radius}
```

它计算了circle所定义圆的周长。

### 正则表达式

如果想要使用正则表达式呢？可以参照下式。

```
#{admin.email matches '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\\.com'}
```

这用来判断email是否是一个邮箱。

### 查询运算

SpEL还提供了查询运算符.?[]，来对一个集合进行过滤，得到集合的一个子集

```
#{JJlin.songs.?[year eq '2008']}
```

除此之外，还可以使用另外两个查询运算符.^[]和.$[]，它们分别查询结果的第一个和最后一个匹配项。

### 投影运算

SpEL提供了投影运算.![]表示将给定集合的某个属性提取出来成为一个新的集合

```
JJlin.songs.!['title']
```

## 例子

下面是一个具体的应用了SpringEL的例子。
我们定义一个男人类，女人类

```
package org.doge.eldemo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Man {

    @Value("Tom")
    private String name;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

```
package org.doge.eldemo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Woman {
    @Value("Marry")
    private String name;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

再定义一个家庭类，一个家包含一个男人和一个女人。

```
package org.doge.eldemo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Family {

    @Value("#{man}")
    public Man husband;

    @Value("#{woman}")
    public Woman wife;
    
    @Override
    public String toString() {
        return "Husband: " +husband.getName() + "\n"
                + "Wife: " + wife.getName();
    }
}
```

设置类

```
package org.doge.eldemo;


import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan
public class ELConfig {

}
```

测试类

```
package org.doge.eldemo;


import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class ELTest {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(ELConfig.class);

        Family family = context.getBean("family", Family.class);
        System.out.println(family);
    }
}
```

运行结果

```
Husband: Tom
Wife: Marry
```

当我们修改一下家庭类，会得到同样的结果

```
package org.doge.eldemo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Family {

    @Value("#{man.name}")
    public String husbandName;

    @Value("#{woman.name}")
    public String wifeName;

    @Override
    public String toString() {
        return "Husband: " +husbandName + "\n"
                + "Wife: " + wifeName;
    }
}

---------------------------或者--------------------------
package org.doge.eldemo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Family {

    public String husbandName;

    public String wifeName;

    public Family(@Value("#{man.name}") String hName,
                  @Value("#{woman.name}") String wName){
        this.husbandName = hName;
        this.wifeName = wName;
    }

    @Override
    public String toString() {
        return "Husband: " +husbandName + "\n"
                + "Wife: " + wifeName;
    }
}
```
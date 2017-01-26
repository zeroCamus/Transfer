---
title: Spring学习笔记之一——松耦合
date: 2017-01-27 21:30:20
categories: 技术
tags: Java
---
面向对象的概念，是一个很好的设计来打破系统进入一个组可重用的对象。然而，当系统变大，尤其是在Java项目，庞大的对象依赖关系将一直紧密耦合引起对象难以管理或修改。在这种情况下，可以使用Spring框架作为一个核心模块轻松高效地管理所有的对象依赖。
<!--more-->
## 耦合度

我们先了解一下耦合度的概念。

> 耦合性也叫块间联系。指软件系统结构中各模块间相互联系紧密程度的一种度量。模块之间联系越紧密，其耦合性就越强，模块之间越独立则越差，模块间耦合的高低取决于模块间[接口](http://baike.baidu.com/view/159864.htm)的复杂性，调用的方式以及传递的信息。
>
> 形象的说，就是要将代码写的和电脑一样，主类就是电脑的主机箱，当程序需要实现什么功能的时候只需要加其他的类引入接口，就像电脑上的usb接口。

## 松耦合

松耦合（解耦和）系统通常是基于消息的系统，此时客户端和远程服务并不知道对方是如何实现的。客户端和服务之间的通讯由消息的架构支配。只要消息符合协商的架构，则客户端或服务的实现就可以根据需要进行更改，而不必担心会破坏对方。松耦合通讯机制提供了紧耦合机制所没有的许多优点，并且它们有助于降低客户端和远程服务之间的依赖性，这在Web开发中体现的尤为明显，下面我们通过一个例子来了解一下松耦合。

## 松耦合实例

假如我们有一堆水果，我们现在想要获取一种水果，我们可以用如下的方法。

我们先定义一个Fruit接口

```
package org.doge.fruit;

public interface Fruit {
    void eat();
}
```

然后定义三种水果:

苹果

```
package org.doge.fruit;

public class Apple implements Fruit{
    @Override
    public void eat() {
        System.out.println("Eating Apple");
    }
}
```

香蕉

```
package org.doge.fruit;

public class Banana implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Banana");
    }
}
```

橘子

```
package org.doge.fruit;

public class Orange implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Orage");
    }
}
```

### 传统方法

```
package org.doge.fruit;

class FruitFactory{
    private Fruit fruit;
    public void getFruit(String fruitName){
        if (fruitName.equals("apple")){
            fruit = new Apple();
        }
        else if (fruitName.equals("orange")){
            fruit = new Orange();
        }
        else if (fruitName.equals("banana")){
            fruit = new Banana();
        }
    }

    public void eatFruit() {
        this.fruit.eat();
    }
}
public class FruitTestOne {
    public static void main(String[] args) {
        FruitFactory f = new FruitFactory();
        f.getFruit("orange");
        f.eatFruit();
    }
}
```

在以上代码中，可以看出，当我们输入水果的名字时，就可以吃到对应的水果，可是，假如我们要增加水果，除了要定义新的水果类之外，我们还必须修改`FruitFactory`类，增加一个`else if`选项，这就导致了`FruitFactory`类和水果类之间的耦合度过大，修改一个的同时也要修改另一个，不利于代码的扩充和程序的复用。下面我们给出一个改进方法。

### 传统方法的改进方法

我们利用Java的反射机制，重写一下`FruitFactory`类。

```
package org.doge.fruit;

class FruitFactory{
    private Fruit fruit;
    public void getFruit(String fruitName) throws ClassNotFoundException{
        Class<?> cls = Class.forName(fruitName);
        try{
            fruit = (Fruit)cls.newInstance();
        }
        catch (Exception e){}
    }

    public void eatFruit() {
        this.fruit.eat();
    }
}
public class FruitTestOne {
    public static void main(String[] args) throws Exception{
        FruitFactory f = new FruitFactory();
        f.getFruit("org.doge.fruit.Banana");
        f.eatFruit();
    }
}
```

从以上的代码我们可以看出，即使我们新增了水果类，`FruitFactory`类也察觉不出来，我们可以不加改动的继续使用它，这就是松耦合的一个方法。下面我们再给出另一个方法。

### 利用Spring框架实现松耦合

```
package org.doge.fruit;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

class EatFruitHelper{
    Fruit fruit;

    public void setFruit(Fruit fruit) {
        this.fruit = fruit;
    }

    public void eatFruit(){
        this.fruit.eat();
    }
}

public class FruitTest {
    public static void main(String[] args){
        ApplicationContext context =
                new ClassPathXmlApplicationContext("demo.xml");
        EatFruitHelper helper = (EatFruitHelper) context.getBean("eatFruitHelper");
        helper.eatFruit();
    }
}
```

定义一个`demo.xml`

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="eatFruitHelper" class="org.doge.fruit.EatFruitHelper">
        <property name="fruit" ref="apple"/>
    </bean>
    <bean id="orange" class="org.doge.fruit.Orange" />
    <bean id="apple" class="org.doge.fruit.Apple" />
    <bean id="banana" class="org.doge.fruit.Banana" />
</beans>
```

运行：

```
十月 09, 2016 11:21:35 上午 org.springframework.context.support.ClassPathXmlApplicationContext prepareRefresh
信息: Refreshing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Sun Oct 09 11:21:35 CST 2016]; root of context hierarchy
十月 09, 2016 11:21:35 上午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [demo.xml]
Eating Apple
```

当我们将`demo.xml`中`eatFruitHelper`的`properoty`的`ref`值由”apple”改为”banana”时，再次运行，就会得到以下输出

```
十月 09, 2016 11:25:55 上午 org.springframework.context.support.ClassPathXmlApplicationContext prepareRefresh
信息: Refreshing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Sun Oct 09 11:25:55 CST 2016]; root of context hierarchy
十月 09, 2016 11:25:55 上午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [demo.xml]
Eating Banana
```

可见，我们甚至不需要改变源代码中的设置，不在源代码中new对象，只需要将xml文件对应的值进行更改，将对象的创建和销毁任务交给spring容器，就可以得到不同的对象，达到松耦合的目的。

## 总结

从上述代码中我们可以看出，在Java中，各个模块间产生耦合的一个很重要的因素就是new操作符的使用，而在Spring中，通过控制反转(IoC)，将实例化对象的任务由程序员转移到了Spring容器，Spring容器可以统一管理这种实例化频繁的操作，极大的减小了模块之间的耦合度。
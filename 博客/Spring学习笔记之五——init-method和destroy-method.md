---
title: Spring学习笔记之五——init-method和destroy-method
date: 2017-01-27 21:30:24
categories: 技术
tags: Java
---

在某些特定的业务需求中，我们需要在bean的初始化和Ioc容器关闭的时候执行某些动作，这时我们可以利用`init-method` 和`destroy-method`。
<!--more-->
我们先来定义一个`MessageService`类

```
package org.doge.initdemo;

public class MessageService {
    private String message;

    public void setMessage(String message) {
        this.message = message;
    }

    public void init(){
        System.out.println("Init message: " + message);
    }

    public void destroy(){
        System.out.println("destroy");

    }
}
```

假如我们希望当bean初始化之后调用init方法，bean销毁时执行destroy方法，我们可以利用`init-method` 和`destroy-method`，我们在配置文件中这样设置

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="messageservice" class="org.doge.initdemo.MessageService"
    init-method="init" destroy-method="destroy">
        <property name="message" value="Hello" />
    </bean>

</beans>
```

如上代码，我们指定`init-method`为`init`方法，`destroy-method`为`destroy`方法。然后我们再编写一个测试类。

```
package org.doge.initdemo;

public class MessageService {
    private String message;

    public void setMessage(String message) {
        this.message = message;
    }

    public void init(){
        System.out.println("Init message: " + message);
    }

    public void destroy(){
        System.out.println("destroy");

    }
}
```

运行，得到以下结果

```
十月 15, 2016 8:34:31 下午 org.springframework.context.support.ClassPathXmlApplicationContext prepareRefresh
信息: Refreshing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Sat Oct 15 20:34:31 CST 2016]; root of context hierarchy
十月 15, 2016 8:34:32 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [initdemo.xml]
Init message: Hello
---------------------------
十月 15, 2016 8:34:32 下午 org.springframework.context.support.ClassPathXmlApplicationContext doClose
destroy
信息: Closing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Sat Oct 15 20:34:31 CST 2016]; root of context hierarchy
```

可以看到，当我们给`message`赋值为`Hello`时，运行了`init`方法，当我们关闭`context`时，运行了`destroy`方法。

在一些比较旧的版本中， 也会使用`InitializingBean` 和 `DisposableBean`接口来达到以上目的，但这会使代码与配置文件紧密的耦合，所以我们不提倡使用这种方法。
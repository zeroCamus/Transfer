---
title: Spring学习笔记之四——Required依赖检查
date: 2017-01-27 21:30:23
categories: 技术
tags: Java
---
bean 配置文件用于确定的特定类型(基本，集合或对象)的所有属性被设置。在大多数情况下，你只需要确保特定属性已经设置（但不是所有属性），使用XML配置时，有时你需要的属性没有设置，但是程序运行的时候并不会抛出异常，所以，为了保证你需要的属性必须被设置，可以使用@Required注解来实现依赖检查。
<!--more-->
我们先定义一个Person类

```
package org.doge.checkdemo;

import org.springframework.beans.factory.annotation.Required;

public class Person {
    private String name;
    private int age;

    public void setName(String name) {
        this.name = name;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

再定义一个测试类

```
package org.doge.checkdemo;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class checktest {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("checkdemo.xml");
        Person p = context.getBean("person", Person.class);
    }

}
```

假如我们在设置中只配置一个属性

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
	   http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="person" class="org.doge.checkdemo.Person">
        <property name="age" value="12" />

    </bean>
</beans>
```

然后运行程序，并没有发生任何异常，虽然我们没有设置name，但是程序却能正常的编译运行，这有时会带来许多麻烦，为了保证某些属性必须被设置，我们来使用@require注解。

```
package org.doge.checkdemo;

import org.springframework.beans.factory.annotation.Required;

public class Person {
    private String name;
    private int age;

    @Required
    public void setName(String name) {
        this.name = name;
    }

    @Required
    public void setAge(int age) {
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

我们将name和age的Setter方法全部打上@Required注解，然后在配置文件中包含``

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
	   http://www.springframework.org/schema/beans/spring-beans.xsd
	   http://www.springframework.org/schema/context
	   http://www.springframework.org/schema/context/spring-context.xsd">

    <context:annotation-config />
    <bean id="person" class="org.doge.checkdemo.Person">
        <property name="age" value="12" />

    </bean>
</beans>
```

同样的，我们只设置一个`age`属性，然后我们再次运行程序。

这时就会抛出一个`BeanInitializationException`异常，提示我们`Property 'name' is required for bean 'person'`。这样，我们就达到了依赖检查的目的。
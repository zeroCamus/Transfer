---
title: Spring学习笔记之二——依赖注入（DI)
date: 2017-01-27 21:30:21
categories: 技术
tags: Java
---
Spring通过一种称作控制反转（IoC）的技术促进了松耦合。当应用了IoC，一个对象依赖的其它对象会通过被动的方式传递进来，而不是这个对象自己创建或者查找依赖对象。依赖注入（DI）是IoC的一种方式，在上一节《松耦合》中我们已经接触到了它的概念，这次我们来具体了解一下。
<!--more-->
## 依赖注入的方法

- `Setter方法注入`：通过控制类的Set方法传入参数实现注入。
- `构造器注入`：通过控制类的构造器实现注入。

## 实例

定义一个接口`Animal`。

```
package org.doge.animal;

public interface Animal {
    void bark();
    String getName();
}
```

定义动物`狗`。

```
package org.doge.animal;

public class Dog implements Animal {
    private String name;
    private String breed;
    
    public void setName(String name) {
        this.name = name;
    }
    
    public void setBreed(String breed) {
        this.breed = breed;
    }
    
    public Dog(){}
    
    public Dog(String name, String breed){
        this.name = name;
        this.breed = breed;
    }
    
    @Override
    public void bark() {
        System.out.println(this.breed + " " + this.name + ": Wang~ Wang~ Wang~");
    }
    
    public String getBreed() {
        return this.breed;
    }

    public String getName() {
        return this.name;
    }
}
```

定义动物`猫`。

```
package org.doge.animal;

public class Cat implements Animal {
    private String name;
    private String breed;

    public void setName(String name) {
        this.name = name;
    }

    public void setBreed(String breed) {
        this.breed = breed;
    }
    
    public Cat(){}
    
    public Cat(String name, String breed){
        this.name = name;
        this.breed = breed;
    }
    
    @Override
    public void bark() {
        System.out.println(this.breed + " " + this.name + ": Miao~ Miao~ Miao~");
    }
    
    public String getBreed() {
        return this.breed;
    }

    public String getName() {
        return this.name;
    }
}
```

### Setter方法注入

假如我们要取一条叫Tom，品种为哈士奇的狗，让狗叫

```
package org.doge.animal;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class AnimalTest {
    public static void main(String[] args) {
        ApplicationContext context =
                new ClassPathXmlApplicationContext("animaldemo.xml");
        Animal a = (Animal)context.getBean("dog");
        a.bark();
    }
}
```

建一个`animaldemo.xml`写入

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="dog" class="org.doge.animal.Dog" >
        <property name="name" value="Tom" />
        <property name="breed" value="Huskies" />
    </bean>
    <bean id="cat" class="org.doge.animal.Cat" />
</beans>
```

输出

```
十月 09, 2016 4:46:42 下午 org.springframework.context.support.ClassPathXmlApplicationContext prepareRefresh
信息: Refreshing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Sun Oct 09 16:46:42 CST 2016]; root of context hierarchy
十月 09, 2016 4:46:43 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [animaldemo.xml]
Huskies Tom: Wang~ Wang~ Wang~
```

我们再新建一个`Dinner`类，表示吃晚餐，类内有一个私有变量`meat`，表示晚餐要吃的肉。

```
package org.doge.animal;

public class Dinner {
    private Animal meat;
    public void setMeat(Animal meat) {
        this.meat = meat;
    }
    public void eat(){
        System.out.println("Eating " + this.meat.getName());
    }
    public Dinner(){}
    public Dinner(Animal meat){
        this.meat = meat;
    }
}
```

将`animaldemo.xml`修改如下

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="dog" class="org.doge.animal.Dog" >
        <property name="name" value="Tom" />
        <property name="breed" value="Huskies" />
    </bean>
    <bean id="dinner" class="org.doge.animal.Dinner">
        <property name="meat" ref="dog" />
    </bean>
    <bean id="cat" class="org.doge.animal.Cat" />
</beans>
```

写一个测试运行一下

```
package org.doge.animal;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class AnimalTest {
    public static void main(String[] args) {
        ApplicationContext context =
                new ClassPathXmlApplicationContext("animaldemo.xml");
        Dinner a = (Dinner)context.getBean("dinner");
        a.eat();
    }
}
```

结果如下

```
十月 09, 2016 6:09:24 下午 org.springframework.context.support.ClassPathXmlApplicationContext prepareRefresh
信息: Refreshing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Sun Oct 09 18:09:24 CST 2016]; root of context hierarchy
十月 09, 2016 6:09:24 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [animaldemo.xml]
Eating Tom
```

观察两次对`animaldemo.xml`的修改，能发现如果我们想利用`Setter`方法注入，就要给被注入的`bean`新增一个`property`标签，标签里的`name`属性代表需要被注入的成员变量名，`value` 和`ref`属性代表赋给该变量的值。使用`value`属性名的意思是把`value`属性的值赋给该成员变量，使用`ref`属性名的意思是把`ref`属性所指向的`bean`赋给该成员变量。

### 构造器方法注入

我们保持源代码不变，修改`animaldemo.xml`

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="dog" class="org.doge.animal.Dog" >
        <property name="name" value="Tom" />
        <property name="breed" value="Huskies" />
    </bean>
    <bean id="dinner" class="org.doge.animal.Dinner">
        <constructor-arg>
            <ref bean="dog" />
        </constructor-arg>
    </bean>
    <bean id="cat" class="org.doge.animal.Cat" />
</beans>
```

运行程序，结果不变。

观察以上修改，能发现我们只需要给被注入的`bean`一个`constructor-arg`属性，属性内填入需要注入的值，就能实现构造器方法注入。
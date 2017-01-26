---
title: Spring学习笔记之六——JavaConfig
date: 2017-01-27 21:30:25
categories: 技术
tags: Java
---
随着Spring版本的更新，`JavaConfig`已经成为了Spring的核心模块，现在官方比较提倡的是尽量使用`JavaConfig`来替代`XmlConfig`，我们来了解一下`JavaConfig`，并且在以后的学习中，尽量多的使用`JavaConfig`。

（到现在为止，博主还没学到`自动装配`和`组件扫描`，所以关于一些高阶的`JavaConfig`，放到以后来总结）
<!--more-->
我们先定义一个水果接口

```
package org.doge.configtest;

public interface Fruit {
    void eat();
}
```

定义苹果类

```
package org.doge.configtest;

public class Apple implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Apple");
    }
}
```

定义橘子类

```
package org.doge.configtest;

public class Orange implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Orange");
    }
}
```

编写`JavaConfig`

```
package org.doge.configtest;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FruitConfig {
    @Bean(name = "apple")
    public Fruit apple(){
        return new Apple();
    }
}
```

对于配置类，我们将它打上`@Configuration`注解。对于要配置的Bean我们可以将打上`@Bean`注解，注解里的name=…相当于xml配置里的id=…。

编写一个测试类。

```
package org.doge.configtest;

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class App {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(FruitConfig.class);
        Fruit fruit = context.getBean("apple", Fruit.class);
        fruit.eat();
    }
}
```

结果

```
Eating Apple
```

如果我们编写了多个设置类，那么如何在一个设置类内引用其他设置类呢？我们可以使用`@Import`注解，参数为要引用的类（以数组的形式传入）。
假如我们还编写了一个`OrangeConfig`类，用于配置橘子Bean。然后我们在`FruitConfig`类中使用`@Import`注解如下。

```
package org.doge.configtest;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration
@Import({OrangeConfig.class})
public class FruitConfig {
    @Bean(name = "apple")
    public Fruit apple(){
        return new Apple();
    }
}
```

这样我们就可以通过`FruitConfig`获得apple和orange的Bean了。我们来编写一个测试

```
package org.doge.configtest;

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class App {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(FruitConfig.class);
        Fruit fruit = context.getBean("orange", Fruit.class);
        fruit.eat();
    }
}
```

结果

```
Eating Orange
```

假如要配置为Bean的类中有成员变量，我们该怎么办呢？
下面我们给苹果类加入几个新方法和变量

```
package org.doge.configtest;

public class Apple implements Fruit {

    private String name;

    public void setName(String name) {
        this.name = name;
    }

    public Apple(String name){
        setName(name);
    }

    public Apple(){}

    @Override
    public void eat() {
        System.out.println("Eating Apple " + name);
    }
}
```

为了给Bean注入一些值，我们可以编写如下的Config类

```
package org.doge.configtest;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration
@Import({OrangeConfig.class})
public class FruitConfig {
    @Bean(name = "apple")
    public Fruit apple(){
        Apple temp = new Apple();
        temp.setName("White apple");
        return temp;
    }
}


或者

@Configuration
@Import({OrangeConfig.class})
public class FruitConfig {
    @Bean(name = "apple")
    public Fruit apple(){
        return new Apple("White apple");
    }
}
```

运行测试，都会输出

```
Eating Apple White apple
```

如果想要注入Bean，也是很简单的。我们加一个Eater类，并简化Apple类

```
public class Apple implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Apple!");
    }
}

public class Eater {

    private Fruit fruit;

    public Eater(){}
    public Eater(Fruit fruit){
        this.fruit = fruit;
    }

    public void eatFruit(){
        this.fruit.eat();
    }
}
```

我们就可以这样修改Config

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class EatConfig {

    @Bean
    public Apple apple(){
        return new Apple();
    }

    @Bean
    public Orange orange(){
        return new Orange();
    }

    @Bean
    public Eater eater(){
        return new Eater(orange());
    }
}
```

就会得到预期输出

```
Eating Orange
```

注意，因为orange()被@bean标注了，Spring会直接拦截所有对它的调用，并确保直接返回该方法所创建的bean，而不是每次都对其进行实际的调用。

关于更多的JavaConfig，会在以后的学习中继续总结。
---
title: Spring学习笔记之七——自动化装配Bean
date: 2017-01-27 21:30:26
categories: 技术
tags: Java
---
尽管通过Java或者XML等显式方式来装配Spring非常有用，但是在便利性方面，最方便的还是Spring的自动化配置。如果Spring能进行完全的自动化装配的话，那何苦还要显式的将这些bean装配在一起呢？

（从本章开始，博主开始逐渐用JavaConfig代替XMLConfig）
<!--more-->
## 什么是自动化装配

Spring从两个角度来实现自动化装配。

- 组件扫描：Spring会自动发现应用的上下文中所创建的bean。
- 自动装配：Spring自动满足bean之间的依赖。

如果将二者结合起来，就能发挥出强大的威力，它们能将显式配置降到最低。

## 组件扫描

组件扫描最常用的是@Component注解，**如果给一个类打上该注解，就可以被自动地识别为一个Bean，而不用在设置中显式的声明**。

我们先给出几个类

```
public interface Fruit {
    void eat();
}

public class Apple implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Apple!");
    }
}

public class Orange implements Fruit {
    @Override
    public void eat() {
        System.out.println("Eating Orange");
    }
}
```

我们用常规的方式给他们配置Bean

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

}
```

编写一个测试类运行一下

```
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class App {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(EatConfig.class);
        Fruit f = context.getBean("apple", Fruit.class);
        f.eat();
    }
}
```

结果

```
Eating Apple!
```

可以看出，我们需要在设置中显示的配置好Bean，这次我们使用组件扫描。

首先我们把苹果和橘子类打上@Component注解（代码略），然后修改设置，把苹果和橘子类抹掉，然后给设置加上@ComponentScan注解（如果想要指定被扫描的包，可以用@ComponentScan({“package1”, “package2”})的方式），打开组件扫描。

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@ComponentScan
@Configuration
public class EatConfig {
}
```

然后我们再次运行测试。得到如下输出

```
Eating Apple!
```

可以看出，虽然我们没有在设置中显式的配置Bean，但是由于@Component注解的原因，测试仍然可以通过，这说明Spring通过隐式的扫描装配了Bean。

## 自动装配

我们再给出一个Eater类，Eater类内部包含有一个Fruit对象和eaterFruit方法。

```
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

如果我们想要给Eater注入Bean，我们可以这样写配置

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

从上述设置中可以看出我们给Eater注入了一个Orange，修改测试代码，并运行。

```
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class App {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(EatConfig.class);
        Eater e = context.getBean("eater", Eater.class);
        e.eatFruit();
    }
}
```

结果

```
Eating Orange
```

可以看出，我们为了实现这么一个小的功能，却多写了这么多的代码，为了减小编码负担，我们可以使用组件扫描+自动装配的方式，实现自动化装配。

要想实现自动装配，我们需要使用@Autowired注解。假如我们想要让一个属性自动装配，我们可以给他打上@Autowired注解，当打上该注解的时候，Spring会自动在所有的Bean中选择符合依赖条件的Bean，将其注入该属性中。

我们再次修改代码

将橘子的@Component注解去掉，只保留苹果的。然后修改Eater代码

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Eater {

    @Autowired
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

再修改设置代码

```
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@ComponentScan
@Configuration
public class EatConfig {
}
```

运行测试

```
Eating Apple!
```

可以看出，我们在设置类中并没有编写任何具体的内容就实现了扫描和注入，这就是自动化装配。

需要注意的是，我们这里只将苹果和橘子中的一个打上了注解，这是因为如果我们将二者都打上注解，二者就都可以被组件扫描到，而二者都满足自动注入的条件，Spring就会无法选择，并抛出NoUniqueBeanDefinitionException异常。

但是，如果由于业务需要，需要将同一个接口的众多实现类都装配为Bean，为了保证扫描器能正常工作，我们可以将要注入Bean打上@Primary注解，比如说在本例中我们可以将苹果和橘子类都加上@Component注解，但给苹果类加一个额外的@Primary注解。
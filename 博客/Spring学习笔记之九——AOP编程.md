---
title: Spring学习笔记之九——AOP编程
date: 2017-01-27 21:30:28
categories: 技术
tags: Java
---
AOP（Aspect-Oriented Programming），名字与 OOP 仅差一个字母，其实它是对 OOP 编程方式的一种补充，翻译过来就是“面向切面编程”。Spring中目前提供了四种类型的AOP支持：

- 基于代理的经典Spring AOP
- 纯POJO切面
- @AspectJ注解驱动的切面
- 注入式Aspec

我们这次分享的是基于注解和JavaConfig的AOP。
<!--more-->
## 引例

我们先来看一个例子。

首先定义一个接口Sleepable

```
package org.doge.aopdemo;

interface Sleepable {
    void closeEyes();
    void sleep();
    void getUp(boolean isComfortable) throws Exception;
}
```

写一个实现类SleepCat

```
package org.doge.aopdemo;

import org.springframework.stereotype.Component;

@Component
public class SleepCat implements Sleepable {

    @Override
    public void sleep() {
        System.out.println("Cat is sleeping!!");
    }

    @Override
    public void closeEyes() {
        System.out.println("Cat is closing its eyes!!");
    }

    @Override
    public void getUp(boolean isComfortable) throws Exception{
        if(isComfortable)
            System.out.println("Cat has got up");
        else
            throw new Exception();
    }
```

写一个切面类

```
package org.doge.aopdemo;

import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class SleepHelper {

    @Before("execution(* org.doge.aopdemo.SleepCat.sleep(..))")
    public void beforeSleep() throws Exception{
        System.out.println("-----------Ready to sleep-----------");
    }

    @AfterReturning("execution(* org.doge.aopdemo.SleepCat.getUp(..))")
    public void afterGetUp(){
        System.out.println("-----------Have a good sleep-----------");
    }

    @AfterThrowing("execution(* org.doge.aopdemo.SleepCat.getUp(..))")
    public void afterFalseGetUp(){
        System.out.println("-----------Have a bad sleep-----------");
    }

}
```

这段代码可以在sleep方法执行前先输出 “———–Ready to sleep———–”，在getUp方法执行后输出”———–Have a good sleep———–” 或 “———–Have a bad sleep———–”。

我们编写 Config类

```
package org.doge.aopdemo;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

@ComponentScan
@Configuration
@EnableAspectJAutoProxy
public class AopConfig {

}
```

写一个测试类

```
package org.doge.aopdemo;

import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class AopTest {
    @Test
    public void aopTest() throws Exception{
        ApplicationContext context = new AnnotationConfigApplicationContext(AopConfig.class);
        Sleepable cat = context.getBean("sleepCat", Sleepable.class);
        cat.closeEyes();
        cat.sleep();
        try{
            cat.getUp(true);
            cat.getUp(false);
        }
        catch (Exception  e){}
    }
}
```

输出结果

```
Cat is closing its eyes!!
-----------Ready to sleep-----------
Cat is sleeping!!
Cat has got up
-----------Have a good sleep-----------
-----------Have a bad sleep-----------
```

## 定义切面

观察以上代码，实现类实现了三个方法，闭眼，睡觉，起床，现在我们想要在睡觉或起床 前做一些其他的事情，但我们可以在SleepCat中添加对应的方法，但是，SleepCat类应该只关心睡觉本身，如果加入了一些其他辅助方法，会让这个类变得臃肿。所以我们可以通过切点的方式，将特定的方法绑定到SleepCat的某个方法上 ，即用代理类封装了目标类，当我们调用SleepCat的某些方法时，代理会拦截到方法调用，在执行该方法之前，会执行切面逻辑，从而实现对现有方法的补充 。

![image](pic\spring1.png)

那如何定义切面呢？从上述代码可以看到，如果想要声明一个切面，我们只需给它加上@Aspect注解，然后在对应的方法上打上对应的通知注解，下面是常见的通知注解。

| 注解              | 通知             |
| --------------- | -------------- |
| @After          | 目标方法返回或抛出异常后执行 |
| @AfterReturning | 目标方法返回后执行      |
| @AfterThrowing  | 目标方法抛出异常执行     |
| @Around         | 将目标方法环绕        |
| @Before         | 目标方法前执行        |

通知注解内跟上的是一个表达式，表达的是这个注解的作用对象 ，比如上面的execution表达式，需要用”*”开头，代表返回任意类型，后面的(..)代表参数是任意类型 （也可以填上对应的类型 ），以上代码就测试了After，Before注解。

下面我们再来测试一下@Around方法 。

## 环绕通知

我们先定义一个CDPlay接口。

```
package org.doge.aopdemo;

public interface CDPlayer {
    void play();
}
```

写一个实现类

```
package org.doge.aopdemo;


import org.springframework.stereotype.Component;

@Component("vinylcd")
public class VinylCD implements CDPlayer {
    @Override
    public void play() {
        System.out.println("Playing");
    }
}
```

编写切面

```
package org.doge.aopdemo;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class CDHelper {
    @Pointcut("execution(* org.doge.aopdemo.VinylCD.play(..))")
    public void point(){}

    @Around("point()")
    public void aroundPlay(ProceedingJoinPoint jp)throws Exception{
        try{
            System.out.println("Open the CD");
            jp.proceed();
            System.out.println("Close the CD");
        }
        catch (Throwable e){}
    }

}
```

注意，编写@Around注解时，我们需要给方法传入一个ProceedingJoinPoint对象，这个对象是必须要有的，因为你要在通知中用它来调用被通知的方法。通知方法中可以做任何方法，当要将控制权交给被通知的方法时，可以调用ProceedingJoinPoint的processed()方法。

下面是设置类

```
package org.doge.aopdemo;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

@ComponentScan
@Configuration
@EnableAspectJAutoProxy
public class CDConfig {
}
```

写一个测试类

```
package org.doge.aopdemo;


import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class CDTest {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(CDConfig.class);
        CDPlayer cd = context.getBean("vinylcd", CDPlayer.class);
        cd.play();
    }
}
```

输出结果

```
Open the CD
Playing
Close the CD
```

可以看出，在play方法调用前后，分别执行了其他的方法。

## 通过注解引入新功能

通过切面，我们甚至还可以为类添加新的功能。我们知道，Java是静态语言，类在编译完成之后，就很难为其增加新的方法。但是我们可以利用Spring代理 ，为目标类引入新的接口 ，当引入接口的方法被调用时，代理会把此调用委托给实现新接口的某个其他对象。实际上，一个Bean的实现被拆分到了多个类中。

![image](pic\spring2.png)
我们来写个测试一下，先写一个要引入的接口Checkable

```
package org.doge.aopdemo;

public interface Checkbale {
    void check();
}
```

写一个实现类

```
package org.doge.aopdemo;

public class CheckVinylCD implements Checkbale {
    @Override
    public void check() {
        System.out.println("Checking CD Player...");
    }
}
```

编写切面

```
package org.doge.aopdemo;

import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.DeclareParents;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class CDHelper {
    @DeclareParents(value = "org.doge.aopdemo.CDPlayer+",
            defaultImpl = CheckVinylCD.class)
    public static Checkbale checkbale;

}
```

编写测试方法

```
package org.doge.aopdemo;


import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class CDTest {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(CDConfig.class);
        CDPlayer cd = context.getBean("vinylcd", CDPlayer.class);
        Checkbale  c= (Checkbale)cd;
        c.check();
    }
}
```

输出如下

```
Checking CD Player...
```

可以看出，我们通过了切面的方式，为vinylcd类引入了新的接口。
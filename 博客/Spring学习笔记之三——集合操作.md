---
title: Spring学习笔记之三——集合操作
date: 2017-01-27 21:30:22
categories: 技术
tags: Java
---
我们来总结一下通过XML配置来进行一些集合操作。
<!--more-->
Spring支持List,Set.Map等集合的装配操作。假设我们有如下类。

```
package org.doge.coldemo;

import java.util.List;
import java.util.Map;
import java.util.Set;

public class Col {
    private List<String> stringList;
    private Set<String> stringSet;
    private Map<String, String> stringStringMap;

	...... 
	Setter和Getter方法
	......
}
```

我们可以创建`coldemo.xml`文件来驱动。

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans 		   http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="col" class="org.doge.coldemo.Col">
        <property name="stringList">
            <list>
                <value>1</value>
                <value>2</value>
                <value>3</value>
            </list>
        </property>
        <property name="stringSet">
            <set>
                <value>one</value>
                <value>two</value>
                <value>three</value>
                <value>four</value>
            </set>
        </property>
        <property name="stringStringMap">
            <map>
                <entry key="name" value="Tom" />
                <entry key="height" value="184" />
                <entry key="professional" value="CS" />
            </map>
        </property>
    </bean>
</beans>
```

如以上代码可知，我们可以用以下标签来表示各种集合

```
- List – <list/>
- Set – <set/>
- Map – <map/>
```

我们编写测试代码来测试一下

```
package org.doge.coldemo;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class ColTest {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("coldemo.xml");
        Col c = context.getBean("col", Col.class);
        System.out.println(c.getStringList());
        System.out.println(c.getStringSet());
        System.out.println(c.getStringStringMap());
    }
}
```

结果

```
十月 10, 2016 4:51:31 下午 org.springframework.context.support.ClassPathXmlApplicationContext prepareRefresh
信息: Refreshing org.springframework.context.support.ClassPathXmlApplicationContext@68de145: startup date [Mon Oct 10 16:51:31 CST 2016]; root of context hierarchy
十月 10, 2016 4:51:31 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [coldemo.xml]
[1, 2, 3]
[one, two, three, four]
{name=Tom, height=184, professional=CS}
```

当我们需要使用具体的集合类（比如List的ArrayList或Map的HashMap）时，我们可以使用util模式来达到目的。我们修改配置文件为如下。

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
	   http://www.springframework.org/schema/beans/spring-beans-2.5.xsd
	   http://www.springframework.org/schema/util
	   http://www.springframework.org/schema/util/spring-util-2.5.xsd">


    <bean id="col" class="org.doge.coldemo.Col">
        <property name="stringList">
            <util:list list-class="java.util.ArrayList">
                <value>1</value>
                <value>2</value>
                <value>3</value>
            </util:list>
        </property>

        <property name="stringSet">
            <util:set set-class="java.util.HashSet">
                <value>one</value>
                <value>two</value>
                <value>three</value>
                <value>four</value>
            </util:set>
        </property>

        <property name="stringStringMap">
            <util:map map-class="java.util.HashMap">
                <entry key="name" value="Tom" />
                <entry key="height" value="184" />
                <entry key="professional" value="CS" />
            </util:map>
        </property>
    </bean>
</beans>
```

再次运行，发现结果不变。

需要注意的是，使用util模式时，不要忘记了在beans中包涵util模式，否则会出错。
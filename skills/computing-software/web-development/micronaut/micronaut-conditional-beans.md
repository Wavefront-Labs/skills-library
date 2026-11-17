---
id: computing-software.web-development.micronaut.micronaut-conditional-beans
name: micronaut-conditional-beans
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, conditional-beans, requires, bean-configurations, configuration, package-info, meta-annotation, debug-logging]
level: practitioner
status: docs-checked
description: "Load Micronaut beans conditionally with @Requires on classes, beans, properties, environments, resources and OS; group conditions with @Configuration and debug unloaded beans."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/conditionalBeans.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/beanConfigurations.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make a bean load only when classpath, configuration, environment or other beans permit.

## Basic use

Repeat `@Requires` for several conditions:

```java
@Singleton
@Requires(beans = DataSource.class)
@Requires(property = "datasource.url")
public class JdbcBookService implements BookService { ... }
```

Reuse a combination through a meta-annotation:

```java
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.PACKAGE, ElementType.TYPE})
@Requires(beans = DataSource.class)
@Requires(property = "datasource.url")
public @interface RequiresJdbc {}
```

Then annotate beans with `@RequiresJdbc`.

## Requirement options

| Requirement | Example |
|---|---|
| class present / absent | `@Requires(classes=javax.servlet.Servlet)` / `@Requires(missing=javax.servlet.Servlet)` |
| bean present / absent | `@Requires(beans=javax.sql.DataSource)` / `@Requires(missingBeans=javax.sql.DataSource)` |
| environment | `@Requires(env="test")` / `@Requires(notEnv="test")` |
| configuration package | `@Requires(configuration="foo.bar")` / `@Requires(missingConfigurations="foo.bar")` |
| SDK version | `@Requires(sdk=Sdk.JAVA, value="1.8")` |
| entities via package scanning | `@Requires(entities=javax.persistence.Entity)` |
| property set / missing | `@Requires(property="data-source.url")` / `@Requires(missingProperty="data-source.url")` |
| file / classpath resource | `@Requires(resources="file:/path/to/file")` / `@Requires(resources="classpath:myFile.properties")` |
| operating system | `@Requires(os={Requires.Family.WINDOWS})` / `@Requires(notOs={Requires.Family.WINDOWS})` |
| another bean present / its property set | `@Requires(bean=Config.class)` / `@Requires(bean=Config.class, beanProperty="enabled")` |

## Property value checks

```java
@Requires(property="foo")                                      // set
@Requires(property="foo", value="John")                        // equals John
@Requires(property="foo", value="John", defaultValue="John")   // John or unset
@Requires(property="foo", notEquals="Sally")                   // not Sally or unset
```

Bean-property variants take `bean=Config.class, beanProperty="foo"` with optional `value`/`notEquals`. The `Config` bean must be in the context. The getter is checked at compile time. A property counts as present when non-null; primitives hold defaults (`false`, `0`), so they always count as set.

## Group conditions with @Configuration

`@Configuration` on a package (typically `package-info`) groups its beans, and a `@Requires` there applies to all of them:

```groovy
@Configuration
@Requires(beans = javax.sql.DataSource)
package my.package
```

Java and Kotlin can use `package-info.java`; Kotlin has no `package-info.kt` (as of Kotlin 1.3, per the docs).

## Debug why a bean did not load

Enable debug logging for the condition package (see the logging chapter):

```xml
<logger name="io.micronaut.context.condition" level="DEBUG"/>
```

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

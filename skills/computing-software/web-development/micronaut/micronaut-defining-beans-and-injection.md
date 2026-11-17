---
id: computing-software.web-development.micronaut.micronaut-defining-beans-and-injection
name: micronaut-defining-beans-and-injection
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, defining-beans, injection-types, typed-beans, dependency-injection, constructor-injection, beancontext, jakarta-inject]
level: intro
status: docs-checked
description: "Define Micronaut beans with jakarta.inject, pick constructor, field, method or nullable injection, and limit exposed bean types with @Bean(typed)."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/beans.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/how.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/beanContext.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/injection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/injection/constructorInjection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/injection/fieldInjection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/injection/methodInjection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/injection/nullableInjection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/typed.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: declare beans and wire them with the right injection style in a Micronaut application.

## Define and look up a bean

A bean is an object whose lifecycle the IoC container manages. Micronaut implements JSR-330, so use the `jakarta.inject` annotations.

```java
public interface Engine {
    int getCylinders();
    String start();
}

@Singleton
public class V8Engine implements Engine { /* ... */ }

@Singleton
public class Vehicle {
    private final Engine engine;
    public Vehicle(Engine engine) { this.engine = engine; }
}
```

Programmatic lookup: `ApplicationContext context = ApplicationContext.run(); Vehicle vehicle = context.getBean(Vehicle.class);`. `BeanContext` is the container of all bean definitions; normally you use annotations instead of calling it.

No runtime reflection is needed: annotation processors (Java) or AST transformations (Groovy) generate `BeanDefinition` classes ahead of time, so injection points are known at build time.

## Choose an injection type

- Constructor injection is the recommended style: allows immutable types, needs no extra annotation, less likely to give a `NullPointerException`. With several constructors, mark one with `@Inject` or `@Creator` (`@Creator` can also select a `static` factory method). With neither, Micronaut uses the first `public` constructor, else compilation fails.
- Field injection: `@Inject Engine engine;`. Final fields are a compile error. Private fields are injected by reflection, which is not recommended.
- Method injection: annotate a method with `@Inject`; every argument is resolved as a bean, and an unresolvable one throws `NoSuchBeanException`. Private methods use reflection. Useful for post-construction initialisers but generally avoid it.
- A private constructor with `@Inject`/`@Creator` also needs `@ReflectiveAccess`, otherwise compilation fails; such a type cannot have AOP advice.
- Multiple candidates for one argument without a qualifier give `NonUniqueBeanException`.

Exclude classes, fields or methods from injection with `@Vetoed`.

## Optional injection

Annotate the injected type with `org.jspecify.annotations.Nullable` and `null` is injected when no bean exists (Kotlin: a `?` type):

```java
Vehicle(@Nullable Engine engine) {
    this.engine = engine != null ? engine : Engine.create(6);
}
```

Works for constructor, method and field injection; for fields/methods handle `null` in a `@PostConstruct` method. `@Nullable` cannot be used on primitives with configuration injection; use `@Bindable(defaultValue="..")` instead.

## Limit injectable types

By default a scoped bean is injectable as its class, all interfaces and superclasses. Restrict this with `@Bean(typed=...)`; the class must implement the listed type or compilation fails:

```java
@Singleton
@Bean(typed = Engine.class)
public class V8Engine implements Engine { /* ... */ }
```

Then `beanContext.getBean(V8Engine.class)` throws `NoSuchBeanException`, while `getBean(Engine.class)` returns the `V8Engine`.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

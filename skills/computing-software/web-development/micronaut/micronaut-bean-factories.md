---
id: computing-software.web-development.micronaut.micronaut-bean-factories
name: micronaut-bean-factories
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, factories, factory, bean-fields, primitive-beans, disabledbeanexception, injectionpoint, prototype]
level: practitioner
status: docs-checked
description: "Expose third-party or computed objects as Micronaut beans with @Factory methods and @Bean fields, including primitive beans, conditional disabling and InjectionPoint use."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/factories.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make a class you cannot annotate (e.g. from a library) available as a bean.

## Factory methods

Annotate a class with `@Factory`; methods carrying a scope annotation produce beans whose type is the method's return type. Method parameters are resolved as beans.

```java
@Factory
class EngineFactory {
    @Singleton
    Engine v8Engine(CrankShaft crankShaft) {
        return new V8Engine(crankShaft);
    }
}
```

- The factory itself is a singleton destroyed with the context; use `@Prototype` scope to dispose it after it produces a bean.
- A factory may have many bean methods, each returning a distinct type. Do not call one bean method from another inside the class; inject the type as a parameter instead.
- To close the produced bean on context shutdown, put `@Bean(preDestroy = "methodName")` on the factory method.
- If a bean method/field declares its own scope or qualifier, those of the type are omitted; the factory instance's qualifiers are not inherited by its beans.

## Beans from fields (3.0+)

`@Bean` on a field produces a bean. Discouraged versus factory methods, but handy for test mocks:

```java
@MicronautTest
public class VehicleMockSpec {
    @Requires(beans = VehicleMockSpec.class)
    @Bean @Replaces(Engine.class)
    Engine mockEngine = () -> "Mock Started";
    @Inject Vehicle vehicle;
}
```

Only public or package-protected fields work for non-primitive types; `static`, `private` or `protected` fields are a compilation error.

## Primitive and array beans (3.1+)

```java
@Factory
class CylinderFactory {
    @Bean @Named("V8") final int v8 = 8;
    @Bean @Named("V6") final int v6 = 6;
}
// inject: public V8Engine(@Named("V8") int cylinders)
```

Limits: no AOP advice on primitives or wrappers, hence no proxying custom scopes, and `@Bean(preDestroy=..)` is unsupported.

## Programmatically disabling a bean

A factory method may throw `DisabledBeanException`. Prefer `@Requires`; use the exception only when `@Requires` cannot express it:

```java
@EachBean(EngineConfiguration.class)
public Engine buildEngine(EngineConfiguration engineConfiguration) {
    if (engineConfiguration.isEnabled()) {
        return engineConfiguration::getCylinders;
    } else {
        throw new DisabledBeanException("Engine configuration disabled");
    }
}
```

## Using the injection point

A factory method can take `InjectionPoint<?>` to read annotation metadata of where the bean is injected:

```java
@Factory
class EngineFactory {
    @Prototype
    Engine v8Engine(InjectionPoint<?> injectionPoint, CrankShaft crankShaft) {
        final int cylinders = injectionPoint.getAnnotationMetadata()
                .intValue(Cylinders.class).orElse(8);
        // return V6Engine or V8Engine, else throw IllegalArgumentException
    }
}
```

Used with `Vehicle(@Cylinders(6) Engine engine)`. The factory must be `@Prototype` so the method runs per injection point; for singleton engines keep a `Map` so each is built once.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

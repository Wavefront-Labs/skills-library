---
id: computing-software.web-development.micronaut.micronaut-around-advice
name: micronaut-around-advice
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, around-advice, aop, method-interceptor, interceptor-binding, proxy-target, factory]
level: practitioner
status: docs-checked
description: "Write Micronaut Around advice: a binding annotation plus a MethodInterceptor, member-based binding, proxy generation options and advice on @Factory beans."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/aroundAdvice.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decorate method behaviour at compile time with an annotation and a `MethodInterceptor`.

## 1. Binding annotation

```java
@Documented
@Retention(RUNTIME)          // must be RUNTIME
@Target({TYPE, METHOD})      // class or method level
@Around                      // marks it as Around advice
public @interface NotNull {
}
```

## 2. Interceptor

```java
@Singleton
@InterceptorBean(NotNull.class)   // ties the interceptor to the annotation
public class NotNullInterceptor implements MethodInterceptor<Object, Object> {
    @Nullable
    @Override
    public Object intercept(MethodInvocationContext<Object, Object> context) {
        Optional<Map.Entry<String, MutableArgumentValue<?>>> nullParam = context.getParameters()
            .entrySet().stream()
            .filter(entry -> Objects.isNull(entry.getValue().getValue()))
            .findFirst();
        if (nullParam.isPresent()) {
            throw new IllegalArgumentException("Null parameter [" + nullParam.get().getKey() + "] not allowed");
        }
        return context.proceed();   // continue the invocation
    }
}
```

`@InterceptorBean` is meta-annotated with `@Singleton`; add `@Prototype` if each intercepted bean needs its own interceptor. Interceptors use no reflection.

## 3. Apply and test

```java
@Singleton
public class NotNullExample {
    @NotNull
    void doWork(String taskName) { ... }
}
```

Injecting `NotNullExample` yields a compile-time-generated proxy (a subclass). The page's test expects `IllegalArgumentException` with message `Null parameter [taskName] not allowed` from `doWork(null)`. Per the page, keep the advice in a dependent JAR so it compiles before the code that uses it.

## Binding by annotation members

`@InterceptorBinding(bindMembers = true)` on the binding annotation makes member values part of the match; mark members to ignore with `@NonBinding`. For repeatable annotations add `matchAllOccurrences = true` (experimental): every occurrence on the interceptor must be on the target, and occurrences on a method replace those on its class.

```java
@Repeatable(Audits.class)
@Around
@InterceptorBinding(bindMembers = true, matchAllOccurrences = true)
public @interface Audit {
    String value();
    @NonBinding String reason() default "";
}
```

## Proxy options on @Around

- `proxyTarget` (default false): delegate to the original bean instance instead of subclassing.
- `hotswap` (default false): like `proxyTarget` plus `HotSwappableInterceptedProxy`, with a `ReentrantReadWriteLock` around each call so the target can be swapped.
- `lazy` (default false): resolve the proxy target per call instead of eagerly.

## Advice on @Factory beans

Advice on the `@Factory` class (type level) advises the factory itself, not the beans it makes. Advice on a method that carries a scope annotation (e.g. `@Prototype @Timed`) advises the produced bean's public methods, not its creation. Method-level advice on the factory class is not possible; make methods non-public to exclude them.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

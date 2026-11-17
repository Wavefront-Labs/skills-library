---
id: computing-software.web-development.micronaut.micronaut-introduction-and-adapter-advice
name: micronaut-introduction-and-adapter-advice
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, introduction-advice, adapter-advice, aop, method-interceptor, event-listener, stub]
level: practitioner
status: docs-checked
description: "Implement Micronaut Introduction advice that supplies method implementations for interfaces, and Adapter advice that turns annotated methods into SAM beans."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/introductionAdvice.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/adapterAdvice.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have the framework implement abstract types (Introduction) or generate a bean from an annotated method (Adapter).

## Introduction advice

Unlike Around advice it provides the implementation rather than decorating. Examples named by the docs: Spring Data and the Micronaut `@Client` annotation.

```java
@Introduction   // introduction advice
@Bean           // types annotated with @Stub become beans
@Documented
@Retention(RUNTIME)
@Target({TYPE, ANNOTATION_TYPE, METHOD})
public @interface Stub {
    String value() default "";
}
```

```java
@Singleton
@InterceptorBean(Stub.class)
public class StubIntroduction implements MethodInterceptor<Object, Object> {
    @Nullable
    @Override
    public Object intercept(MethodInvocationContext<Object, Object> context) {
        return context.getValue(Stub.class, context.getReturnType().getType()).orElse(null);
    }
}
```

```java
@Stub
public interface StubExample {
    @Stub("10")
    int getNumber();
    LocalDateTime getDate();
}
```

The page's test: `getNumber()` returns 10 and `getDate()` returns null. All abstract methods go to the interceptor.

- If the interceptor cannot implement a method, call `proceed()` on the `MethodInvocationContext`: other introduction interceptors may implement it, and an `UnsupportedOperationException` is thrown if none can.
- With several introduction advices, override `getOrder()` on `MethodInterceptor` to set priority.

## Adapter advice

`@Adapter` makes a method into an implementation of a SAM (single abstract method) interface. `@EventListener` is the built-in example:

```java
@EventListener
void onStartup(StartupEvent event) {
    // startup logic here
}
```

It generates an `ApplicationEventListener` that calls the method. The annotation itself is just:

```java
@Documented
@Retention(RUNTIME)
@Target({ElementType.ANNOTATION_TYPE, ElementType.METHOD})
@Adapter(ApplicationEventListener.class)   // SAM type to adapt
@Indexed(ApplicationEventListener.class)
@Inherited
public @interface EventListener {
}
```

Generic types of the SAM interface are aligned automatically. To build your own, define an annotation with `@Adapter(YourSamType.class)`.

### Which advice applies to the generated bean

The adapter is a separate bean that only delegates. Advice declared on the class holding the adapted method is not applied to the adapter (it would run twice). Advice on the adapted method itself still runs (e.g. `@Retryable` on an `@EventListener` method keeps retrying). Advice on the SAM interface stays on the adapter.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

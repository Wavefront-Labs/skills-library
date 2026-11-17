---
id: computing-software.web-development.micronaut.micronaut-interceptor-life-cycle
name: micronaut-interceptor-life-cycle
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, interceptor-lifecycle, interceptor-scope, prototype, per-target, interception-target, ordering]
level: advanced
status: docs-checked
description: "Choose Micronaut interceptor scope (singleton vs per-target), bind kinds, use lazyInterceptorsPerTarget, inject InterceptionTarget and order interceptors."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/interceptorLifecycle.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide how many instances of a stateful interceptor exist and how long they live.

## Kinds and what they require

| Kind | Applies to | Target needs |
|---|---|---|
| `AROUND` | every intercepted method | `@Around` |
| `INTRODUCTION` | every abstract method | `@Introduction` |
| `AROUND_CONSTRUCT` | constructor | `@AroundConstruct` |
| `POST_CONSTRUCT` | `@PostConstruct` methods | `@InterceptorBinding(kind = POST_CONSTRUCT)` |
| `PRE_DESTROY` | `@PreDestroy` methods | `@InterceptorBinding(kind = PRE_DESTROY)` |

Only `ConstructorInterceptor` beans run for `AROUND_CONSTRUCT`; only `MethodInterceptor` beans for the others; a plain `Interceptor` is eligible for every kind it is bound to. An interceptor runs only for kinds it is bound to: binding one kind does not imply the others.

## Scope

`@InterceptorBean` is meta-annotated `@Singleton`: one shared instance, so it must not hold per-bean state. Declare `@Prototype` (or another non-singleton scope) and you get one instance per intercepted bean, reused across all kinds, so state set at construction is still there at destruction:

```java
@Prototype
@InterceptorBinding(value = Tracked.class, kind = InterceptorKind.AROUND_CONSTRUCT)
@InterceptorBinding(value = Tracked.class, kind = InterceptorKind.POST_CONSTRUCT)
@InterceptorBinding(value = Tracked.class, kind = InterceptorKind.PRE_DESTROY)
public class TrackingInterceptor implements Interceptor<Object, Object> {
    private Registration registration;
    @Override
    public Object intercept(InvocationContext<Object, Object> context) {
        MethodInvocationContext<?, ?> method = (MethodInvocationContext<?, ?>) context;
        if (method.getKind() == InterceptorKind.POST_CONSTRUCT) {
            registration = Tracker.register(method.getTarget());
        } else if (method.getKind() == InterceptorKind.PRE_DESTROY) {
            registration.close();
        }
        return context.proceed();
    }
}
```

Sequence for one bean: interceptors resolved once at creation; `AROUND_CONSTRUCT` then constructor; injection; `POST_CONSTRUCT` then callbacks; `AROUND`/`INTRODUCTION` per call; `PRE_DESTROY` then callbacks. A non-singleton interceptor is destroyed as a dependent of the target, so its own `@PreDestroy` runs after the target's.

## Proxy targets

With `@Around(proxyTarget = true)` (this includes every scoped proxy such as `@RequestScope`, `@ThreadLocal`, `@Refreshable`, and advised beans from `@Factory` methods) the proxy resolves interceptors once, so a non-singleton interceptor is one per proxy, shared by all its targets. For one per target, set `lazyInterceptorsPerTarget`:

```java
@Retention(RUNTIME)
@Around(proxyTarget = true, lazyInterceptorsPerTarget = true)
public @interface Audited { }
```

Each target (for example each `@Refreshable` target created by a `RefreshEvent`) then has its own `@Prototype` interceptor, so a call counter restarts after refresh. For a scoped bean whose binding annotation has no `@Around` of its own, declare `@Around(proxyTarget = true, lazy = true, lazyInterceptorsPerTarget = true)`, because an `@Around` on the bean replaces the one its scope contributes.

Edge case from the page: a `@Prototype` with `@AroundConstruct` advice and no proxy, created with `createBean` and destroyed with `destroyBean(Object)`, has no registration in the context, so `PRE_DESTROY` resolves a new interceptor.

## Knowing the target

A non-singleton interceptor can inject `InterceptionTarget`; its `definition()` carries the intercepted bean's qualifier, which tells apart targets such as two `@EachBean` beans:

```java
@Prototype
@InterceptorBean(Labelled.class)
public class LabelInterceptor implements MethodInterceptor<Object, String> {
    private final String label;
    public LabelInterceptor(InterceptionTarget target) {
        this.label = target.definition().getDeclaredQualifier() instanceof Named named
            ? named.getName() : target.definition().getBeanType().getSimpleName();
    }
    @Override
    public String intercept(MethodInvocationContext<Object, String> context) {
        return "[" + label + "] " + context.proceed();
    }
}
```

The target is not known to singleton or custom-scoped interceptors, or to interceptors obtained by a plain lookup: a `@Nullable` injection point gets `null`, any other fails with `NoSuchBeanException`.

## Ordering

Interceptors run in ascending order, the same for every kind. Implement `io.micronaut.core.order.Ordered` and return, e.g., `10` to run before an interceptor returning `20`.

After upgrading, recompile intercepted classes; beans compiled by an earlier version resolve an interceptor per interception point.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

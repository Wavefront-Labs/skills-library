---
id: computing-software.web-development.micronaut.micronaut-debugging-dependency-injection
name: micronaut-debugging-dependency-injection
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, debugging-di, injection-trace, bean-resolution-tracer, startup-time, serviceloader, diagnostics]
level: advanced
status: docs-checked
description: "Trace Micronaut bean creation and timing with MICRONAUT_INJECT_TRACE and custom BeanResolutionTracer implementations registered on the builder or via ServiceLoader."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/iocDebugging.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/iocDebugging/beanResolutionTracers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: see what Micronaut creates at startup, from where, and how long it takes.

## Injection trace mode

Set the environment variable `MICRONAUT_INJECT_TRACE` to a regex of classes to trace:

```bash
MICRONAUT_INJECT_TRACE=.+ ./gradlew run
MICRONAUT_INJECT_TRACE=.+ ./mvnw mn:run
```

Output includes the application's configuration profile, the applicable configuration and its source, and the beans created, where, and how long creation took. It can also be activated through `ApplicationContextBuilder`.

## Custom tracer

The mode is built on the experimental `BeanResolutionTracer` API. Callbacks: `traceBeanCreation` (start), `traceBeanCreated` (end) or `traceBeanCreationFailed`, plus `traceInjectBean` and `traceInjectComplete` around each injection point. They come in pairs on the resolving thread and nest like a call stack, so keep open spans on a per-thread stack. Each receives a `Resolution` (`getBeansInCreation()`, `getInjectionPath()`); an `Injection` gives kind, declaring bean, member name, argument and qualifier. Beans from `createBean` are traced too.

```java
public class TimingTracer implements BeanResolutionTracer {
    private final ThreadLocal<Deque<Long>> starts = ThreadLocal.withInitial(ArrayDeque::new);
    private final Map<String, Long> timings = new ConcurrentHashMap<>();

    @Override
    public void traceBeanCreation(Resolution resolution, BeanDefinition<?> definition, Argument<?> beanType) {
        starts.get().push(System.nanoTime());
    }
    @Override
    public void traceBeanCreated(Resolution resolution, BeanDefinition<?> definition) {
        long took = System.nanoTime() - starts.get().pop();
        timings.put(definition.getBeanType().getName(), took);
    }
    @Override
    public void traceBeanCreationFailed(Resolution resolution, BeanDefinition<?> definition, Throwable failure) {
        starts.get().pop();   // keep the stack balanced
    }
    @Override
    public void traceInjectBean(Resolution resolution, Injection injection) { }
}
```

Register it before any bean exists (a tracer cannot be a bean):

```java
ApplicationContext context = ApplicationContext.builder()
    .beanResolutionTracer(tracer)
    .start();
```

## Tracers from libraries

Provide a `BeanResolutionTracerProvider` listed in `META-INF/services/io.micronaut.context.BeanResolutionTracerProvider`. Every provider is instantiated at context start (keep the constructor cheap); its tracer is only created when `isEnabled` returns true, which by default it does not. Enable discovered tracers with the `micronaut.inject.trace.tracers` system property, `MICRONAUT_INJECT_TRACE_TRACERS` env var, or `ApplicationContextBuilder.beanResolutionTracerDiscovery(true)`. A provider can also self-enable:

```java
public boolean isEnabled(Activation activation) {
    return activation.isDiscoveryEnabled()
        || activation.getEnvironmentNames().contains(Environment.DEVELOPMENT);
}
```

## Rules

- All active tracers get every callback; discovered tracers run in provider order (`Ordered`). The `MICRONAUT_INJECT_TRACE` patterns restrict only the trace mode's output, not your tracers.
- Callbacks run on the hot resolution path: keep them fast, never throw or create beans in one. An exception from a tracer fails the resolution being traced.
- With no tracer active, no tracing work is done.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

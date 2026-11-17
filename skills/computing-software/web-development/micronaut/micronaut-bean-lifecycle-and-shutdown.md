---
id: computing-software.web-development.micronaut.micronaut-bean-lifecycle-and-shutdown
name: micronaut-bean-lifecycle-and-shutdown
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, life-cycle, graceful-shutdown, postconstruct, predestroy, dependson, dependent-beans, gracefulshutdowncapable]
level: practitioner
status: docs-checked
description: "Run Micronaut code at bean construction and destruction with @PostConstruct, @PreDestroy and @Bean(preDestroy), order shutdown with @DependsOn, and enable graceful shutdown."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/lifecycle.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/gracefulShutdown.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: initialise and clean up beans in the right order, and stop the application gracefully.

## Construction

```java
@Singleton
public class V8Engine implements Engine {
    private boolean initialized = false;
    @PostConstruct   // jakarta.annotation.PostConstruct
    public void initialize() { initialized = true; }
}
```

The method runs once the object is constructed and fully injected. Scopes control when construction happens.

## Destruction

```java
@Singleton
public class PreDestroyBean implements AutoCloseable {
    @PreDestroy   // jakarta.annotation.PreDestroy
    @Override
    public void close() throws Exception { ... }
}
```

Runs when the context closes. Alternatively name the method in `@Bean(preDestroy = "flush")` on the class (the method must be public with no arguments, otherwise compilation fails). For factory beans, set it on the factory method or field: `@Bean(preDestroy = "stop") @Singleton public Connection connection()`.

Note: implementing `Closeable`/`AutoCloseable` alone does not make Micronaut close the bean; use one of the methods above.

## Destruction order

Singletons are destroyed in dependency order: a bean before the beans injected into it (constructor, method or field), so `@PreDestroy` can still use its dependencies. For beans that do not inject each other, declare the ordering:

```java
@Singleton
@DependsOn(MessagePublisher.class)   // created after, destroyed before, the publisher
public class MessageConsumer {
    @PreDestroy void stop() { ... }
}
```

`@DependsOn` also works on factory methods and accepts interfaces (every implementing bean is created before and destroyed after). Unconnected beans are destroyed in bean-name order, so the sequence is stable between runs. For shutdown logic spanning several beans, use `@EventListener` methods for `ShutdownEvent` (published before any bean is destroyed), orderable with `@Order`.

## Dependent beans

Beans used to construct your bean are dependent beans; if their scope is `@Prototype` or unknown they are destroyed with your instance. For dynamic lookups that the consumer should own, inject `BeanDependencyResolver` and call `dependencies.getBean(Worker.class)`; newly created prototypes are destroyed after the consumer's destruction callbacks. The resolver must be injected into a managed consumer. See the page for `createBeanRegistration`, `createDependencyGroup()` and `withDependencies(group -> ...)` for explicit ownership and early destruction.

## Graceful shutdown

Meaning: no new HTTP connections; existing connections serve no new requests but in-progress ones finish; scheduled tasks stop running while in-progress ones finish.

Enable with the property `micronaut.lifecycle.graceful-shutdown.enabled=true`; it then triggers automatically on `ApplicationContext.stop()`. For control, use the `GracefulShutdownManager` API. Status and the count of active tasks can be read through the health management endpoint.

For your own beans implement `GracefulShutdownCapable`: `shutdownGracefully` triggers shutdown and returns a future completing when done; optionally implement `reportActiveTasks` to report a count for the health endpoint.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

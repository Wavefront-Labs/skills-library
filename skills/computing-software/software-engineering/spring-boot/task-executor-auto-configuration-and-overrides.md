---
id: computing-software.software-engineering.spring-boot.task-executor-auto-configuration-and-overrides
name: task-executor-auto-configuration-and-overrides
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, task-execution, asynctaskexecutor, applicationtaskexecutor, enableasync, virtual-threads, asyncconfigurer]
level: practitioner
status: docs-checked
description: "How Boot auto-configures an AsyncTaskExecutor, which integrations use applicationTaskExecutor, backing off for custom Executor beans and spring.task.execution.mode=force."
sources:
  - https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With no `Executor` bean, Boot auto-configures an `AsyncTaskExecutor`: a virtual-thread `SimpleAsyncTaskExecutor` when virtual threads are enabled (Java 21+ and `spring.threads.virtual.enabled=true`), otherwise a `ThreadPoolTaskExecutor` with sensible defaults. It is used, unless a custom `Executor` bean is defined, for: `@EnableAsync` (unless an `AsyncConfigurer` bean exists), Spring for GraphQL `Callable` return values, Spring MVC async request handling, Spring WebFlux blocking execution, Spring WebSocket message channels, the JPA bootstrap executor, and background bean initialization.

Back-off: registering a custom `Executor` bean makes the auto-configured executor back off and the custom one serves regular `@EnableAsync` execution. But Spring MVC, WebFlux and GraphQL require a bean named `applicationTaskExecutor` (type `AsyncTaskExecutor` for MVC and WebFlux; GraphQL does not enforce the type). WebSocket and JPA use an `AsyncTaskExecutor` if a single bean of that type exists or one is named `applicationTaskExecutor`. The context bootstrap executor uses `applicationTaskExecutor` unless a bean named `bootstrapExecutor` exists. `applicationTaskExecutor` is also used for regular tasks if there is no `@Primary` bean or `taskExecutor`-named `Executor`/`AsyncConfigurer`. If neither the auto-configured executor nor `applicationTaskExecutor` exists, regular execution uses a bean named `taskExecutor` (not used for MVC, WebFlux, GraphQL; usable by WebSocket and JPA if it is an `AsyncTaskExecutor`).

Helpers: `ThreadPoolTaskExecutorBuilder` and `SimpleAsyncTaskExecutorBuilder` build instances replicating the default behaviour. For multiple executors (the page's example), define an `applicationTaskExecutor` bean for MVC/WebFlux/WebSocket/JPA and a separate bean named `taskExecutor` for regular `@EnableAsync` execution. If a `taskExecutor`-named bean is not an option, mark your bean `@Primary` or define an `AsyncConfigurer` bean instead.

Keep the auto-configured executor alongside a custom one: declare the custom `Executor` bean with `@Bean(defaultCandidate=false)` and inject it with `@Qualifier` plus `@Autowired`. Or force auto-configuration:
```yaml
spring:
  task:
    execution:
      mode: force
```
With `force`, the auto-configured executor is used for all the integrations above even when a custom or `@Primary` `Executor` exists, including regular `@EnableAsync` tasks, which can then only be overridden with an `AsyncConfigurer` bean.

## Checked

2026-11-07. Read features/task-execution-and-scheduling.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Rewrote the multiple-executors sentence to follow the page's example: applicationTaskExecutor plus a bean named taskExecutor, with @Primary or AsyncConfigurer only when a taskExecutor-named bean is not an option. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.

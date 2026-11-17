---
id: computing-software.software-engineering.spring-boot.application-events-and-runners
name: application-events-and-runners
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, application-events, applicationlistener, commandlinerunner, applicationrunner, exitcodegenerator, shutdown-hook]
level: practitioner
status: docs-checked
description: "Order of SpringApplication events, registering early listeners, CommandLineRunner and ApplicationRunner ordering, and ExitCodeGenerator for exit codes."
sources:
  - https://docs.spring.io/spring-boot/reference/features/spring-application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Event order during a run:
1. `ApplicationStartingEvent`: start, before processing except listener and initializer registration
2. `ApplicationEnvironmentPreparedEvent`: Environment known, context not yet created
3. `ApplicationContextInitializedEvent`: initializers called, no bean definitions loaded
4. `ApplicationPreparedEvent`: bean definitions loaded, refresh not started
5. (`WebServerInitializedEvent` and `ContextRefreshedEvent` fall between 4 and 6)
6. `ApplicationStartedEvent`: context refreshed, runners not yet called
7. `AvailabilityChangeEvent` with `LivenessState.CORRECT`
8. `ApplicationReadyEvent`: runners have been called
9. `AvailabilityChangeEvent` with `ReadinessState.ACCEPTING_TRAFFIC`
10. `ApplicationFailedEvent`: exception on startup

Some events fire before the context exists, so register listeners with `SpringApplication.addListeners(...)` or `SpringApplicationBuilder.listeners(...)`, or in `META-INF/spring.factories`: `org.springframework.context.ApplicationListener=com.example.project.MyListener`. Listeners run in the same thread by default, so do not run long tasks; use runners. Events in a child context also reach ancestor contexts, so with a hierarchy a listener can receive the same event type several times; inject the context (`ApplicationContextAware` or `@Autowired`) and compare it with the event's context.

Runners: implement `ApplicationRunner` (takes `ApplicationArguments`) or `CommandLineRunner` (takes `String[]`). The single `run` method is called just before `SpringApplication.run(...)` completes, after startup but before accepting traffic. Order several with `Ordered` or `@Order`.

Exit: each `SpringApplication` registers a JVM shutdown hook so the context closes gracefully (`DisposableBean`, `@PreDestroy` work). Beans or exceptions implementing `ExitCodeGenerator` supply an exit code via `SpringApplication.exit()`, passed to `System.exit()`. With several generators the first non-zero code wins; order with `Ordered` or `@Order`.

## Checked

2026-11-07

Read spring-application.adoc in full (cited SpringApplication page): Application Events and Listeners, Using the ApplicationRunner or CommandLineRunner, Application Exit. The include-code examples for the runner and exit sections were not opened; claims rest on the page prose.
Confirmed: the nine-step event order including both AvailabilityChangeEvent entries (LivenessState#CORRECT, ReadinessState#ACCEPTING_TRAFFIC); WebServerInitializedEvent and ContextRefreshedEvent published after ApplicationPreparedEvent and before ApplicationStartedEvent; addListeners / SpringApplicationBuilder.listeners and the META-INF/spring.factories ApplicationListener entry; same-thread note; child-to-ancestor context publication and the ApplicationContextAware / @Autowired comparison advice; ApplicationRunner (ApplicationArguments) vs CommandLineRunner (string array); ordering with Ordered or @Order; shutdown hook, DisposableBean, @PreDestroy; ExitCodeGenerator on beans and exceptions, first non-zero exit code wins.
Nothing trimmed.

Method: documentation only; no commands were run.

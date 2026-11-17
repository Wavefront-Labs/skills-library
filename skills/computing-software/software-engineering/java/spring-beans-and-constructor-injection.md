---
id: computing-software.software-engineering.java.spring-beans-and-constructor-injection
name: spring-beans-and-constructor-injection
category: computing-software
field: software-engineering
product: java
tags: [java, spring-beans, spring-dependency-injection, component-scanning, constructor-injection, bean-scopes, spring-framework]
level: practitioner
status: docs-checked
description: "Wire Spring beans cleanly: component scanning vs @Bean methods, constructor injection, qualifiers and @Primary, scopes, lifecycle callbacks and circular dependency errors."
sources: ["https://docs.spring.io/spring-framework/reference/core/beans.html", "https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html", "https://docs.spring.io/spring-boot/reference/using/spring-beans-and-dependency-injection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring beans and constructor injection

**Goal:** an application context that is explicit, testable and fails at startup
rather than at runtime.

## Declaring beans
```java
@Service
public class InvoiceService {
    private final InvoiceRepository repo;
    private final Clock clock;
    public InvoiceService(InvoiceRepository repo, Clock clock) {   // single constructor: no @Autowired needed
        this.repo = repo; this.clock = clock;
    }
}

@Configuration
class InfraConfig {
    @Bean Clock clock() { return Clock.systemUTC(); }               // third-party types: @Bean methods
}
```
Component scanning covers the package of the `@SpringBootApplication` class and below;
classes outside it are silently not beans ("No qualifying bean of type ...").

## Why constructor injection
- Final fields, immutable, impossible to construct half-initialised.
- Plain `new InvoiceService(fakeRepo, fixedClock)` in unit tests - no Spring needed.
- Too many constructor params is a visible design smell. Field injection (`@Autowired` on
  fields) hides dependencies and needs reflection in tests.

## Several candidates
```java
@Bean @Primary DataSource primaryDs() { ... }
@Bean @Qualifier("reporting") DataSource reportingDs() { ... }
public ReportService(@Qualifier("reporting") DataSource ds) { ... }
```
Inject all: `List<PaymentProvider>` (ordered by `@Order`) or `Map<String, PaymentProvider>`
(keyed by bean name) for strategy-style dispatch. Optional deps: `ObjectProvider<Foo>`.

## Scopes
Default singleton (one per context; must be thread-safe, no per-request state in fields).
`@Scope("prototype")`, `@RequestScope`, `@SessionScope`. Injecting a shorter-lived bean into a
singleton needs a scoped proxy or `ObjectProvider` - otherwise you get one instance forever.

## Lifecycle
`@PostConstruct` / `@PreDestroy` (jakarta.annotation), `@Bean(initMethod/destroyMethod)`,
`SmartLifecycle` for ordered start/stop, `ApplicationRunner` for startup work after the
context is ready.

## Circular dependencies
Spring Boot 2.6+ fails startup on cycles (`The dependencies of some of the beans in the
application context form a cycle`). Fix the design: extract the shared logic into a third
bean, or publish an event. `spring.main.allow-circular-references=true` restores the old behaviour but hides the design problem.

## Debugging the context
`ApplicationContext.getBeanNamesForType(Foo.class)` lists the beans of a type.

## Checked
2026-10-28: Confirmed in the Spring Framework beans reference and the Spring Boot 2.6 release notes: constructor-based injection and the circular dependency problem, startup failure on cycles from Boot 2.6, and the spring.main.allow-circular-references property. Removed the actuator and --debug lines and the @Lazy claim (pages not fetched).
Method: documentation only; no commands were run.

## Verify
- [ ] No field injection in production classes; services unit-tested with `new`.
- [ ] Context starts in a `@SpringBootTest` smoke test in CI (wiring errors caught early).

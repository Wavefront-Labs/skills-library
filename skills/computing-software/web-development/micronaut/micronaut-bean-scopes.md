---
id: computing-software.web-development.micronaut.micronaut-bean-scopes
name: micronaut-bean-scopes
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, scopes, singleton, prototype, context, refreshable, eager-init, default-scope]
level: practitioner
status: docs-checked
description: "Pick a Micronaut bean scope (Singleton, Context, Prototype, Refreshable...), force eager singleton creation, refresh beans, and define scopes on meta annotations."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/scopes.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/scopes/builtInScopes.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/scopes/builtInScopes/eagerInit.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/scopes/refreshable.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/scopes/metaScopes.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose how many instances of a bean exist and when they are created.

## Built-in scopes

| Annotation | Meaning |
|---|---|
| `@Singleton` | one instance |
| `@Context` | created with the `ApplicationContext` (eager) |
| `@Prototype` | new instance each time it is injected (synonym for `@Bean`, since prototype is the default scope) |
| `@Infrastructure` | cannot be overridden with `@Replaces` |
| `@ThreadLocal` | one bean per thread |
| `@Refreshable` | state refreshed via the `/refresh` endpoint |
| `@RequestScope` | new instance per HTTP request |

Add a custom scope by defining a `@Singleton` bean implementing `CustomScope`.

## Eager creation

`@Singleton` beans are created lazily by default (to optimise startup). Options:

- `@Context` binds the bean to the context lifecycle, so it is created at start.
- `@Parallel` on a `@Singleton` initialises it in parallel without hurting startup time; if it fails to initialise, the application shuts down.
- All singletons, e.g. on AWS Lambda where construction gets more CPU than execution:

```java
Micronaut.build(args)
    .eagerInitSingletons(true)
    .mainClass(Application.class)
    .start();
```

In serverless handlers, override `newApplicationContextBuilder()` and call `builder.eagerInitSingletons(true)`. To eagerly init only configuration beans (`@EachProperty`, `@ConfigurationProperties`, other `@ConfigurationReader` beans) use `.eagerInitConfiguration(true)`.

## Refreshable

```java
@Refreshable
static class WeatherService {
    private String forecast;
    @PostConstruct
    public void init() { forecast = "Scattered Clouds " + new SimpleDateFormat("dd/MMM/yy HH:mm:ss.SSS").format(new Date()); }
    public String latestForecast() { return forecast; }
}
```

The instance is kept until the `/refresh` endpoint is invoked or `applicationContext.publishEvent(new RefreshEvent())` runs; then it is invalidated and a new one is created on next request.

## Scope on a meta annotation

```java
@Requires(classes = Car.class)
@Singleton
@Documented
@Retention(RUNTIME)
public @interface Driver {}
```

Every class annotated `@Driver` is a singleton. That scope cannot be overridden: adding `@Prototype` next to `@Driver` is invalid. To allow overriding, use `@DefaultScope(Singleton.class)` on the annotation instead.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

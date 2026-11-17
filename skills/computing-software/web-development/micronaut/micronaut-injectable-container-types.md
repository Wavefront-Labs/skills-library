---
id: computing-software.web-development.micronaut.micronaut-injectable-container-types
name: micronaut-injectable-container-types
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, container-types, beanprovider, collection-injection, ordering, order-annotation, optional, dependency-injection]
level: practitioner
status: docs-checked
description: "Inject Optional, Collection, Map, Stream, array, Provider or BeanProvider of beans in Micronaut, and control collection and single-bean ordering with @Order."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/types.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: inject several beans, optional beans or lazy handles, and control their order.

## Supported container types (Java, Groovy, Kotlin)

| Type | Injected value |
|---|---|
| `Optional<Engine>` | `empty()` if no bean exists |
| `Collection<Engine>` (or `List`, `Set`...) | all matching beans |
| `Map<String, Engine>` (or subtype) | key is the qualifier |
| `Stream<Engine>` | lazy stream of beans |
| `Engine[]` | native array |
| `jakarta.inject.Provider<Engine>` | for circular dependencies, or a new prototype per `get` call |
| `io.micronaut.context.BeanProvider<Engine>` | same use; the docs recommend it of the three provider types |

A prototype bean gets one instance per injection place; injected as a provider, every `get()` creates a new instance.

## Aggregation gotcha

When a bean injects a `Collection`, `Stream` or array of its own type, it is not a member of that injected collection:

```java
@Singleton
class AggregateEngine implements Engine {
  @Inject List<Engine> engines;   // does not contain AggregateEngine
  public void start() { engines.forEach(Engine::start); }
}
```

## Order an injected collection

Injected collections are unordered by default. Implement `io.micronaut.core.order.Ordered` on the bean type, or, if the type is not `Ordered`, put `@Order` on the beans. `@Order` suits factory-made beans whose class is third-party:

```java
@Factory
public class RateLimitsFactory {
    @Singleton @Order(20)
    LowRateLimit rateLimit2() { return new LowRateLimit(Duration.ofMinutes(50), 100); }
    @Singleton @Order(10)
    HighRateLimit rateLimit1() { return new HighRateLimit(Duration.ofMinutes(50), 1000); }
}
```

Requesting the `RateLimit` collection returns ascending order of the annotation value. `jakarta.annotation.Priority` is mapped to `@Order` at build time, with the same ascending semantics (lower number = higher precedence).

## Pick one bean by order

When injecting a single instance, `@Order` (and so `@Priority`) decides which bean has highest precedence. `Ordered` is not considered here, because that would require instantiating the beans.

Python: the docs list `Optional[Engine]` (None if absent), `list[Engine]` and `dict[str, Engine]`.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

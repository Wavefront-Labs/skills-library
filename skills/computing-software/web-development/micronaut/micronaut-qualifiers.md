---
id: computing-software.web-development.micronaut.micronaut-qualifiers
name: micronaut-qualifiers
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, qualifiers, named, primary, secondary, any, nonbinding, generics, nonuniquebeanexception]
level: practitioner
status: docs-checked
description: "Choose between multiple Micronaut beans of one type with @Named, custom qualifier annotations, annotation members, generic arguments, @Primary, @Secondary and @Any."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/qualifiers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: resolve which implementation is injected when several beans share a type.

## By name

```java
@Inject
public Vehicle(@Named("v8") Engine engine) { this.engine = engine; }
```

Matches because the `@Named` value (`v8`) plus the injected type's simple name (`Engine`) equals, case-insensitively, the bean's simple name (`V8Engine`). `@Named` on a class sets the bean name explicitly.

## By custom annotation

```java
@Qualifier
@Retention(RUNTIME)
public @interface V8 {}
```

Put `@V8` on the bean and at the injection point: `@Inject Vehicle(@V8 Engine engine)`.

## By annotation members (since 3.0)

Members take part in resolution unless marked `@NonBinding`:

```java
@Qualifier
@Retention(RUNTIME)
public @interface Cylinders {
    int value();
    @NonBinding String description() default "";
}
```

Beans: `@Singleton @Cylinders(value = 8, description = "8-cylinder V8 engine")`. Injection: `Vehicle(@Cylinders(8) Engine engine)`.

## By generic type argument (since 3.0)

Given `interface Engine<T extends CylinderProvider>`, `V6Engine implements Engine<V6>` and `V8Engine implements Engine<V8>`, injecting `Engine<V8>` selects `V8Engine`:

```java
@Inject
public Vehicle(Engine<V8> engine) { this.engine = engine; }
```

## Primary and Secondary

`@Primary` on a bean makes it the favoured candidate; `@Secondary` de-prioritises one. Several candidates with no `@Primary` throw `NonUniqueBeanException`.

Tie-breaking order: `@Primary` candidates only (if any); the context's `BeanResolutionCustomizer`; candidates not `@Secondary`; highest `@Order` (unless tied with the next); the `@DefaultImplementation` declared by the first remaining candidate; the candidate whose type is exactly the requested type. Anything left is `NonUniqueBeanException`. `BeanDefinitionRegistry.selectAmong(Argument, Collection)` applies the same rules to your own candidate lists.

## Any

`@Any` injects the first available bean (`@Inject @Any Engine engine;`). Combined with `BeanProvider` it handles absent or multiple beans:

```java
public Vehicle(@Any BeanProvider<Engine> engineProvider) { ... }
void start() { engineProvider.ifPresent(Engine::start); }
void startAll() {
    if (engineProvider.isPresent()) { engineProvider.stream().forEach(Engine::start); }
}
```

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

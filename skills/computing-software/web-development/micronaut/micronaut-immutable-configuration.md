---
id: computing-software.web-development.micronaut.micronaut-immutable-configuration
name: micronaut-immutable-configuration
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, immutable-config, configuration-inject, records, refreshable, configuration-properties]
level: practitioner
status: docs-checked
description: "Write immutable Micronaut configuration as an interface, a @ConfigurationInject constructor or a record, and know how each behaves on refresh."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/immutableConfig.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: bind configuration without setters. Interface-based config needs the `micronaut-context` dependency (already transitive from `micronaut-http`).

## Interface style

```java
@ConfigurationProperties("my.engine")
public interface EngineConfig {

    @Bindable(defaultValue = "Ford")
    @NotBlank
    String getManufacturer();

    @Min(1L)
    int getCylinders();

    @NotNull
    CrankShaft getCrankShaft();

    @ConfigurationProperties("crank-shaft")
    interface CrankShaft {
        Optional<Double> getRodLength();
    }
}
```

Getters delegate to `Environment.getProperty(..)` on every call, so the bean always reflects the current config, including after a refresh, even if injected into a long-lived bean. Only getters (and default methods) are allowed; any other abstract method is a compile error. `Optional` or `@Nullable` makes a value optional.

## Constructor style

```java
@ConfigurationProperties("my.engine")
public class EngineConfig {
    @ConfigurationInject
    public EngineConfig(
            @Bindable(defaultValue = "Ford") @NotBlank String manufacturer,
            @Min(1L) int cylinders,
            @NotNull CrankShaft crankShaft) { /* assign fields */ }

    @ConfigurationProperties("crank-shaft")
    public static class CrankShaft {
        @ConfigurationInject
        public CrankShaft(@Nullable Double rodLength) { /* ... */ }
    }
}
```

`@ConfigurationInject` makes the framework prefer binding config over injecting beans. Binding is skipped for a parameter annotated `@Value`, `@Property`, `@Parameter`, `@Inject`, or whose type carries a bean scope (e.g. `@Singleton`). Works on `@EachProperty` beans too.

## Records

`@ConfigurationProperties("vat") public record ValueAddedTaxConfiguration(@NonNull @NotNull BigDecimal percentage) {}`. The canonical constructor (or a Kotlin data class primary constructor) acts as `@ConfigurationInject`; no annotation is needed. Records bind once, so they behave like the constructor style on refresh.

## Refresh behaviour

Constructor/record beans bind once. Adding `@Refreshable` discards the instance on a refresh event so the next lookup rebuilds it, but it does not update references already injected (for example into a singleton). For long-lived consumers use the interface style, or look the bean up from `BeanContext` when needed. Records are slightly faster than interface getters; let refresh needs decide.

## Defaults

Use `@Bindable(defaultValue = "Ford")` (shown in generated metadata, IDE completion and schema) rather than a language default parameter (works at runtime, invisible to tooling).

## Fluent accessors

Combine with `@AccessorsStyle(readPrefixes = "read")` on the interface and on nested interfaces to name getters `readManufacturer()` etc.

## Validation

With config `my.engine.cylinders=-10` the failure message contains `EngineConfig.cylinders - must be greater than or equal to 1`.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

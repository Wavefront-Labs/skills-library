---
id: computing-software.software-engineering.quarkus.quarkus-cdi-conditional-beans
name: quarkus-cdi-conditional-beans
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, cdi, arc, default-bean, if-build-profile, if-build-property, alternatives]
level: practitioner
status: docs-checked
description: "Swap Quarkus CDI beans by build profile or build property using @DefaultBean, @IfBuildProfile, @UnlessBuildProfile, @IfBuildProperty and selected-alternatives."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/cdi-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional beans in Quarkus CDI

## @DefaultBean

`@io.quarkus.arc.DefaultBean` declares a bean that only applies if no other bean with equal types and qualifiers exists (class, producer or synthetic). Extensions use it to provide overridable defaults; an application overrides one by simply producing its own bean of that type.

```java
@Dependent
public class CustomTracerConfiguration {
    @Produces
    public Reporter reporter() { /* custom */ }
}
```

Default beans may carry `@jakarta.annotation.Priority` (default `@Priority(0)`) to disambiguate several default beans; higher wins.

## Build profile

```java
@Dependent
public class TracerConfiguration {
    @Produces
    @IfBuildProfile("prod")
    public Tracer realTracer(Reporter r, Configuration c) { return new RealTracer(r, c); }

    @Produces
    @DefaultBean
    public Tracer noopTracer() { return new NoopTracer(); }
}
```

`@io.quarkus.arc.profile.UnlessBuildProfile("test")` enables the bean for every profile except `test` (so prod and dev). Both may be put on a stereotype; all conditions must hold.

Gotcha: only the build-time profile counts; the runtime profile has no effect.

## Build properties

`@io.quarkus.arc.properties.IfBuildProperty(name = "some.tracer.enabled", stringValue = "true")` enables a bean when the build-time property has that value; `@UnlessBuildProperty(name = ..., stringValue = "false")` enables it unless it matches. Both are repeatable, may be put on stereotypes, and all conditions must be satisfied.

Gotcha: properties set at runtime have no effect on this resolution.

## Selected alternatives

`beans.xml` is ignored, so select alternatives via configuration:

```properties
quarkus.arc.selected-alternatives=org.acme.Foo,org.acme.*,Bar
```

Match forms are the same as for exclusion (`org.acme.Foo`, `org.acme.*`, `org.acme.**`, simple name `Bar`; for producers the declaring bean class is matched). A match gives the bean priority `Integer#MAX_VALUE`, overriding `@Priority` or a stereotype's priority.

## Checked

2026-11-07. Read in full: cdi-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

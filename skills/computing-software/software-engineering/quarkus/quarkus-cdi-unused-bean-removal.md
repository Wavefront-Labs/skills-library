---
id: computing-software.software-engineering.quarkus.quarkus-cdi-unused-bean-removal
name: quarkus-cdi-unused-bean-removal
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, cdi, arc, unused-beans, unremovable, remove-unused-beans, dev-mode]
level: advanced
status: docs-checked
description: "Understand which Quarkus ArC beans are removed at build time, fix false positives with @Unremovable or unremovable-types, and inspect removals in dev mode."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/cdi-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unused bean removal in Quarkus ArC

By default the container removes unused beans, interceptors and decorators at build time to reduce generated classes and memory. It cannot see programmatic lookup through the static `CDI.current()`, so a bean that is really used may be removed (a false positive); you then see a big warning in the log.

## Controlling the optimization

- `quarkus.arc.remove-unused-beans=none` (or `false`): no removal.
- `quarkus.arc.remove-unused-beans=fwk` (or `framework`): application beans are never removed; non-application classes are optimized normally.

## What counts as unused

Roots are unremovable beans: excluded from removal, named via `@Named`, or declaring an observer method (examples: Jakarta REST resources, beans with `@Scheduled` methods). A bean is unused if it is not unremovable and is not eligible for injection into:

- any injection point in the dependency tree of unremovable beans (including via its producers),
- any `jakarta.enterprise.inject.Instance` or `jakarta.inject.Provider` injection point,
- any `@Inject @All List<>` injection point.

Unused interceptors and decorators are those not associated with any bean.

## Fixing false positives

1. Annotate the class, producer method or producer field with `@io.quarkus.arc.Unremovable`.
2. Or configure it: `quarkus.arc.unremovable-types=org.acme.Foo,org.acme.*,Bar` (fully qualified name, `org.acme.*` package, `org.acme.**` package prefix, or simple name of the bean class).
3. Extension authors: produce an `UnremovableBeanBuildItem`.

## Inspecting in dev mode

- Console: `quarkus.log.category."io.quarkus.arc.processor".level=DEBUG`
- Dev UI page for ArC
- HTTP GET `/q/arc/removed-beans` lists beans removed during build (also `/q/arc`, `/q/arc/beans`, `/q/arc/observers`). Endpoints exist only in dev mode.

Note: strict mode (`quarkus.arc.strict-compatibility=true`) works better with removal disabled for closer spec behaviour.

## Checked

2026-11-07. Read in full: cdi-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

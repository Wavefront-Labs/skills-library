---
id: computing-software.software-engineering.quarkus.quarkus-cdi-bean-discovery-jandex
name: quarkus-cdi-bean-discovery-jandex
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, cdi, arc, bean-discovery, jandex, index-dependency, exclude-types]
level: practitioner
status: docs-checked
description: "Make Quarkus ArC discover beans in dependencies via a Jandex index or quarkus.index-dependency, and exclude types or dependencies from discovery."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/cdi-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bean discovery in Quarkus ArC

Quarkus uses simplified discovery: a single bean archive in `annotated` mode with no visibility boundaries. It is built from application classes, dependencies containing a `beans.xml` (content ignored), dependencies with a Jandex index (`META-INF/jandex.idx`), dependencies named by `quarkus.index-dependency` in `application.properties`, and Quarkus integration code.

Classes without a bean defining annotation are not discovered. Exception: producer methods/fields and observer methods are discovered anyway, and their declaring class is treated as `@Dependent`. Extensions may add rules (e.g. `@Scheduled` methods).

## Index a dependency you control

Add the Jandex plugin. Maven: `io.smallrye:jandex-maven-plugin` with an execution (id `make-index`, goal `jandex`). Gradle: plugin id `org.kordamp.gradle.jandex`.

## Index a dependency you cannot change

```properties
quarkus.index-dependency.acme.group-id=org.acme
quarkus.index-dependency.acme.artifact-id=acme-api
# optional: quarkus.index-dependency.acme.classifier=
```

`acme` is an arbitrary name tying the entries together. If `artifact-id` is omitted, all dependencies with that group id are indexed.

## Exclude types

`quarkus.arc.exclude-types` takes a comma-separated list:

- `org.acme.Foo` - fully qualified class name
- `org.acme.*` - classes in package `org.acme`
- `org.acme.**` - package starts with `org.acme`
- `Bar` - simple class name

```properties
quarkus.arc.exclude-types=org.acme.Foo,org.acme.*,Bar
```

Typical use: a third-party bean that injects a portable extension and breaks under Quarkus.

## Exclude a dependency

```properties
quarkus.arc.exclude-dependency.acme.group-id=org.acme
quarkus.arc.exclude-dependency.acme.artifact-id=acme-services
```

Useful when the artifact would otherwise be scanned, for example because it ships a `beans.xml`.

## Checked

2026-11-07. Read in full: cdi-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

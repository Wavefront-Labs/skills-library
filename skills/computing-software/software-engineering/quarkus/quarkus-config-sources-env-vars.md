---
id: computing-software.software-engineering.quarkus.quarkus-config-sources-env-vars
name: quarkus-config-sources-env-vars
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, configuration, config-sources, environment-variables, application-properties, smallrye-config]
level: practitioner
status: docs-checked
description: "Quarkus config source ordinals, system property and environment variable name conversion, .env files, extra locations, and the dynamic-segment env var pitfall."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus config sources, ordinals and environment variables

Quarkus reads configuration (SmallRye Config, MicroProfile Config) from several sources. A lookup starts at the highest ordinal and falls down until a match is found, so a higher source overrides a lower one per property.

## Default order (ordinal)
1. (400) System properties, e.g. `-Dquarkus.datasource.password=youshallnotpass`
2. (300) Environment variables
3. (295) `.env` file in the current working directory
4. (260) `$PWD/config/application.properties`
5. (250) `application.properties` on the classpath
6. (100) `META-INF/microprofile-config.properties` on the classpath

Each `application.properties` found (including inside jar dependencies) is its own source. In dev mode `config/application.properties` must live in the build output directory (`target` for Maven, `build/classes/java/main` for Gradle); `mvn clean` / `gradle clean` deletes it.

## Environment variable names
For a property such as `foo.BAR.baz` Config tries three names: the exact `foo.BAR.baz`, `foo_BAR_baz` (every non-alphanumeric, non-underscore character becomes `_`), and `FOO_BAR_BAZ` (same, upper-cased). So `quarkus.datasource.password` is `QUARKUS_DATASOURCE_PASSWORD`.
Extra SmallRye rules: quoted segment `foo."bar".baz` becomes `FOO__BAR__BAZ`; dashes `foo.bar-baz` become `FOO_BAR_BAZ`; indexed `foo.bar[0]` becomes `FOO_BAR_0_` and `foo.bar[0].baz` becomes `FOO_BAR_0__BAZ`.

## Gotcha: dynamic segments
`quarkus.datasource."datasource-name".jdbc.url` becomes `QUARKUS_DATASOURCE__DATASOURCE_NAME__JDBC_URL`. If only the env var exists, Quarkus cannot tell whether `DATASOURCE_NAME` means `datasource.name` or `datasource-name`. Declare the dotted name in another source (value may be empty, but must be supplied at runtime or be optional):

```properties
quarkus.datasource."datasource-name".jdbc.url=
```

## `.env` and extra locations
- `.env` holds entries like `QUARKUS_DATASOURCE_PASSWORD=youshallnotpass`, using the same name rules. Do not commit it; it usually has secrets. Its values are not visible via `System.getenv(String)`.
- `quarkus.config.locations` takes comma-separated URIs (`file:`, classpath resource, `jar:`, `http:`). Loaded sources inherit the ordinal of the source that defined `quarkus.config.locations` (system property gives 400). Override per source with `config_ordinal` set inside that source. Sorting: ordinal, then location order, then loading order.

Read config through the Config API, not `System.getProperty` or `System.getenv`, which are not config aware.

## Checked

2026-11-07. Read in full: config-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.quarkus.quarkus-config-yaml
name: quarkus-config-yaml
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, yaml, configuration, profiles, application-yaml, quarkus-config-yaml]
level: intro
status: docs-checked
description: "Use application.yaml in Quarkus with the quarkus-config-yaml extension: profile keys, expressions, external config/application.yaml, and null-key conflicts."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/config-yaml.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YAML configuration in Quarkus

## Enable
Add the extension `io.quarkus:quarkus-config-yaml` (Maven dependency, or Gradle `implementation("io.quarkus:quarkus-config-yaml")`). Then remove `src/main/resources/application.properties` and create `src/main/resources/application.yaml`. If both exist, YAML properties take precedence. Both `.yaml` and `.yml` work; `.yaml` wins over `.yml`. JSON is allowed inside the file, but use one format per file.

```yaml
quarkus:
  datasource:
    db-kind: postgresql
    jdbc:
      url: jdbc:postgresql://localhost:5432/some-database
```

For names that use quotes, do not split the string inside the quotes:

```yaml
quarkus:
  log:
    category:
      "io.quarkus.category":
        level: INFO
```

## Profiles
YAML keys cannot start with `%`, so quote profile keys:

```yaml
quarkus:
  http:
    port: 8081

"%staging":
  quarkus:
    http:
      port: 8082
```

With `staging` active the port is 8082. Profile-aware files `application-{profile}.yaml` also work; an `application.yaml` must exist (even empty) in the same location, and all profile files must use the same extension as the main file.

## Expressions
Same `${...}` syntax as properties; nested keys are referenced with dots:

```yaml
x:
  factor: 2.23694
display:
  unit:
    factor: ${x.factor}
```

## External file
`config/application.yaml` in the working directory (next to the runner) overrides values from the regular `application.yaml`.

## Property conflicts
When one property is the prefix of another (`one.two` and `one.two.three`), use `~` as a null key; null keys are not part of the assembled name:

```yaml
one:
  two:
    ~: 12
    three: 123
```

## Checked

2026-11-07. Read in full: config-yaml.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

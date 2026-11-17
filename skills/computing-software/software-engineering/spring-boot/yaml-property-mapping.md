---
id: computing-software.software-engineering.spring-boot.yaml-property-mapping
name: yaml-property-mapping
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, yaml, snakeyaml, property-flattening, yaml-lists, propertysource-limits]
level: intro
status: docs-checked
description: "How Spring Boot flattens YAML into properties, how lists become [index] keys, what loads YAML directly, and why @PropertySource cannot load YAML."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
YAML is a superset of JSON. `SpringApplication` supports it as an alternative to properties whenever SnakeYAML is on the classpath; `spring-boot-starter` provides it automatically.

Hierarchy is flattened into the Environment:
```yaml
environments:
  dev:
    url: "https://dev.example.com"
    name: "Developer Setup"
```
becomes `environments.dev.url=https://dev.example.com` and `environments.dev.name=Developer Setup`.

Lists use `[index]` keys:
```yaml
my:
  servers:
  - "dev.example.com"
  - "another.example.com"
```
becomes `my.servers[0]=dev.example.com` and `my.servers[1]=another.example.com`. Properties with `[index]` notation bind to `List` or `Set` via the `Binder` class.

Loading YAML directly:
- `YamlPropertiesFactoryBean` loads it as `Properties`.
- `YamlMapFactoryBean` loads it as a `Map`.
- `YamlPropertySourceLoader` loads it as a Spring `PropertySource`.

Limit: YAML files cannot be loaded with `@PropertySource` or `@TestPropertySource`. Use a properties file when you need those annotations.

If `.properties` and YAML exist in the same location, `.properties` takes precedence.

## Checked

2026-11-07. Read features/external-config.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.

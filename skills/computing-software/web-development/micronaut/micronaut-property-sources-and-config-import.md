---
id: computing-software.web-development.micronaut.micronaut-property-sources-and-config-import
name: micronaut-property-sources-and-config-import
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, property-sources, config-import, configuration, yaml, environment-variables]
level: practitioner
status: docs-checked
description: "Know Micronaut's property source priority, import extra files with micronaut.config.import, raise YAML alias limits and handle duplicate classpath config."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/propertySource.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: predict which value wins and bring in extra configuration.

## Priority (highest first)

1. Command line arguments
2. `SPRING_APPLICATION_JSON`
3. `MICRONAUT_APPLICATION_JSON`
4. Java system properties
5. OS environment variables
6. Files from system property `micronaut.config.files` or env `MICRONAUT_CONFIG_FILES` (comma-separated, last wins; absolute file path or `classpath:` prefix). This is ignored inside `bootstrap.yml`/`application.yml`.
7. `application-{environment}.{extension}`
8. `application.{extension}`

`.properties`, `.json`, `.yml` work out of the box (`.groovy` too for Groovy users).

Programmatic sources: pass `PropertySource.of("test", map)` to `ApplicationContext.run(...)`, or register a `PropertySourceLoader` in `META-INF/services/io.micronaut.context.env.PropertySourceLoader`. Calling `enableDefaultPropertySources(false)` on the builder disables the default loaders so only sources added via `propertySources(..)` are used.

Command line: `./gradlew run --args="-endpoints.health.enabled=true -config.property=test"` (Maven: `./mvnw mn:run -Dmn.appArgs="..."`). The `main` must pass `args` on (`Micronaut.run(Application.class, args)`).

## Importing configuration

```yaml
micronaut:
  config:
    import:
      - "file:///etc/myapp/shared"
      - "classpath://overrides.yml"
      - "optional:env://MY_APP_INLINE_CONFIG"
```

- Value may be a string, a list, or indexed (`micronaut.config.import[0]`).
- Protocols: `file://`, `classpath://` (exactly one match, fails on duplicates), `classpath*://` (merges all in classpath order), `env://` (reads the variable value; `.properties` by default, pick format with a name suffix like `MY_APP_INLINE_CONFIG.yml` or `?extension=yml`/`json`), `configtree://`.
- `optional:` skips a missing target; otherwise a `ConfigurationException` is thrown. It does not excuse a placeholder with no default.
- Placeholders with defaults work in locations, e.g. `file://${CONFIG_DIRECTORY:/etc/myapp}/shared.properties`. Entries in one list cannot reference each other; use a nested import.
- `file:///tmp/bar.properties` (three slashes) is the absolute path `/tmp/bar.properties`.
- Without an extension, `.properties`, `.json`, `.yml` (and other enabled loaders) are probed.
- Custom protocol: implement `PropertySourceImporter` (`getProvider()`, `newImportDeclaration(..)`, `importPropertySource(..)`) and list it in `META-INF/services/io.micronaut.context.env.PropertySourceImporter`.

## YAML alias limit

SnakeYAML allows 50 aliases to maps/lists per document; beyond that loading fails with `Number of aliases for non-scalar nodes exceeds the specified max=50`. Raise it with system property `micronaut.config.yaml.max-aliases-for-collections` (or env `MICRONAUT_CONFIG_YAML_MAX_ALIASES_FOR_COLLECTIONS`; the property wins). It cannot be set inside a config file. Only raise it for trusted YAML (billion-laughs risk).

## Duplicate classpath resources

If a configuration file such as `application.yml` is present more than once on the classpath, the `ApplicationContextBuilder` (including `Micronaut`) can be configured to fail fast with an error naming the conflicting locations, take the first match (with an optional warning), or merge all matching resources. The strategy type `FIRST_MATCH` takes the first; `MERGE_ALL` merges duplicates and later resources override earlier ones for the same key. With `MERGE_ALL` only, a `mergeOrder` can order resources by artifact (JAR) name patterns. The exact builder calls are in the page's snippets, which were not readable here; check the `ApplicationContextBuilder` API docs.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against `propertySource.adoc`: the eight-level priority list, `micronaut.config.files` rules, import syntax, protocols, `optional:`, placeholders, three-slash file URL, extension probing, `PropertySourceImporter` methods, YAML alias limit text and precedence, command line examples and duplicate-resource strategies. Removed: the `ResourceLoadStrategy` builder calls and the `mergeOrder` regex example, which the page only shows in unread snippet files.

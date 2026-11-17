---
id: computing-software.web-development.micronaut.micronaut-value-property-injection
name: micronaut-value-property-injection
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, value-annotation, property-annotation, placeholders, environment-variables, random-properties]
level: intro
status: docs-checked
description: "Inject configuration with @Value and @Property, write ${...} placeholders with defaults, understand kebab-case normalization and random values."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/valueAnnotation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/propertySource.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: read single configuration values into beans correctly.

## @Value

`@Value` takes a string that may mix static text and `${...}` placeholders; a default follows `:`.

```java
@Singleton
public class EngineImpl implements Engine {
    @Value("${my.engine.cylinders:6}")
    protected int cylinders;

    @Nullable
    @Value("${my.engine.description}")
    protected String description;
}
```

- Prefer `protected` over `private` fields; private needs reflection.
- A default containing `:` must be wrapped in backticks:

```java
@Value("${my.url:`http://foo.com`}")
URL url;
```

- Static/composed: `@Value("10")`, `@Value("http://${my.host}:${my.port}")` (both properties must exist).
- Placeholders work on any annotation, e.g. `@Controller("${hello.controller.path:/hello}")`, or a configurable client target: `@Client("${my.server.url:`http://localhost:8080`}")` (the backticks are part of the syntax).
- Gotcha: `@Value("my.url")` injects the literal string `my.url`. `@Value` only resolves placeholders inside its text.

## @Property

To inject a named property use `@Property(name = ...)` on a field or setter parameter:

```java
@Singleton
public class Engine {
    @Property(name = "my.engine.cylinders")
    protected int cylinders;

    private String manufacturer;

    @Inject
    public void setManufacturer(@Property(name = "my.engine.manufacturer") String manufacturer) {
        this.manufacturer = manufacturer;
    }
}
```

No default can be given; if the property is missing or not convertible, bean creation fails unless the injection point is `@Nullable`. A sub-tree can be injected as a flattened map: `@Property(name = "jpa.default.properties") Map<String, String> jpaProperties;` yields keys like `hibernate.hbm2ddl.auto`. Use `@MapFormat` to choose nested or flat keys.

## Placeholder rules in configuration files

```yaml
myapp:
  endpoint: http://${micronaut.server.host:localhost}:${micronaut.server.port:8080}/foo
```

- Reference properties in kebab-case (`micronaut.server.default-charset`); camelCase in files is normalized to kebab-case (`myApp.myStuff` -> `my-app.my-stuff`).
- Env vars map flexibly: `MYAPP_MYSTUFF` -> `myapp.mystuff`, `myapp-mystuff`; `MY_APP_MY_STUFF` yields every dot/hyphen combination. You cannot target camelCase or a property containing `_` via env var, and many underscores create exponentially many properties.
- The `Micronaut` builder has methods that control how environment properties participate in configuration (to refine which environment variables are included). They do not affect placeholders, which can still reference any environment variable, even if environment configuration is disabled or the variable is excluded. The method names are in a snippet that was not readable here.
- Secrets: avoid committing them; use env placeholders such as `password: ${JDBC_PASSWORD:}` or a secrets manager.
- Random values: `${random.port}`, `random.int`, `random.integer`, `random.long`, `random.float`, `random.shortuuid` (10 chars, collisions possible), `random.uuid`, `random.uuid2` (no dashes). Ranges: `${random.int[5,10]}` (min inclusive, max exclusive) or `${random.int(5)}`.
- Fail fast: required properties are checked only when a bean is requested; annotate with `@Context` to check at startup (use sparingly).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against `valueAnnotation.adoc` and `propertySource.adoc`: `@Value` placeholder and backtick rules, the static and composed examples, `@Value("my.url")` gotcha, `@Property` behaviour and sub-map example, kebab-case normalisation table, environment variable notes, secrets guidance, the random value table and range syntax, and `@Context` fail-fast. Removed: the three builder method names (`environmentPropertySource`, `environmentVariableIncludes`, `environmentVariableExcludes`), which the page only shows in an unread snippet. The `EngineImpl` and `Engine` samples are illustrative reconstructions of what the page's callouts describe.

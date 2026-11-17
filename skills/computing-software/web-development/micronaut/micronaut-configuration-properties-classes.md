---
id: computing-software.web-development.micronaut.micronaut-configuration-properties-classes
name: micronaut-configuration-properties-classes
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, configuration-properties, type-safe-config, validation, accessors-style, yaml]
level: practitioner
status: docs-checked
description: "Bind type-safe config to a class with @ConfigurationProperties, including nesting, validation, inheritance, includes/excludes and fluent accessors."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/configurationProperties.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: bind a configuration prefix to a mutable, validated class.

```java
@ConfigurationProperties("my.engine")
public class EngineConfig {
    @NotBlank
    private String manufacturer = "Ford";

    @Min(1L)
    private int cylinders;

    private CrankShaft crankShaft = new CrankShaft();

    @ConfigurationProperties("crank-shaft")
    public static class CrankShaft {
        private Optional<Double> rodLength = Optional.empty();
        // getter and setter
    }
    // getters and setters for the outer class
}
```

- The annotation takes the prefix; field defaults serve as default values; static inner classes give nested config (`my.engine.crank-shaft.*`); `Optional` marks optional values; `jakarta.validation` annotations validate.
- Micronaut produces a reflection-free bean and computes property paths at compile time.
- Inject it like any bean (`public EngineImpl(EngineConfig config)`), and supply values through any `PropertySource`:

```java
Map<String, Object> map = new LinkedHashMap<>(1);
map.put("my.engine.cylinders", "8");
ApplicationContext applicationContext = ApplicationContext.run(map, "test");
```

- Use properties in conditions: `@Requires(bean=Config.class, beanProperty="property", value="true")`.
- Inheritance: a subclass annotated `@ConfigurationProperties('bar')` resolves properties under `my.engine.bar`.

## YAML reserved words

Unquoted keys `yes`/`no`, `true`/`false`, `on`/`off` parse as booleans. Quote them (`"yes": "1"`) to keep them strings; this is a YAML/SnakeYAML limit, not Micronaut's.

## includes / excludes

`includes` and `excludes` members filter properties, local and inherited, by property name (setter `setConnectionTimeout` -> `connectionTimeout`).

## Fluent accessors

Since 3.3, `@AccessorsStyle` changes getter/setter prefixes:

```java
@AccessorsStyle(readPrefixes = "", writePrefixes = "")
@ConfigurationProperties("my.engine")
public class EngineConfig {
    private String manufacturer;
    private int cylinders;
    public String manufacturer() { return manufacturer; }
    public void manufacturer(String manufacturer) { this.manufacturer = manufacturer; }
    // same for cylinders
}
```

## Metadata at compile time

Micronaut writes `META-INF/spring-configuration-metadata.json` and a JSON Schema per class under `META-INF/micronaut-configuration-schemas/`. Descriptions come from Javadoc; defaults from `@Bindable(defaultValue)` or a `DEFAULT_<PROPERTY_NAME>` constant (schema). `@NotNull`/`@NotBlank` mark a property required; `@Size`, `@Min`, `@Max`, `@Pattern`, `@Email` etc. map to schema keywords.

`@AllowedValues({"earliest", "latest", "none"})` on a field, setter or record component sets the schema `enum`. It is tooling metadata only: binding does not check it. Add `@Pattern` for runtime validation.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

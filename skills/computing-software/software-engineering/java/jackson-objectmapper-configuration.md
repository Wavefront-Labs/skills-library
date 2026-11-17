---
id: computing-software.software-engineering.java.jackson-objectmapper-configuration
name: jackson-objectmapper-configuration
category: computing-software
field: software-engineering
product: java
tags: [java, java-json, jackson-objectmapper, jackson, javatimemodule, fail-on-unknown-properties, jsoninclude, spring-boot-jackson]
level: practitioner
status: draft
description: "Configure Jackson ObjectMapper safely: java.time support, ISO dates not timestamps, unknown properties policy, null inclusion, BigDecimal, Spring Boot properties and Jackson customizers."
sources: ["https://github.com/FasterXML/jackson-databind/wiki", "https://docs.spring.io/spring-boot/reference/features/json.html#features.json.jackson"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jackson ObjectMapper configuration

Create **one** configured, shared `ObjectMapper` (thread-safe after configuration). In Spring Boot, customise the auto-configured one.

## Spring Boot properties
```yaml
spring.jackson:
  default-property-inclusion: non_null
  serialization:
    write-dates-as-timestamps: false
  deserialization:
    fail-on-unknown-properties: false     # Boot default is false; plain Jackson default is true
    use-big-decimal-for-floats: true
  time-zone: UTC
```
`jackson-datatype-jsr310` (JavaTimeModule) is auto-registered in Boot when on the classpath (starter includes it).

## Manual configuration
```java
ObjectMapper mapper = JsonMapper.builder()
    .addModule(new JavaTimeModule())
    .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)         // ISO-8601 strings
    .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)       // tolerant reader
    .enable(DeserializationFeature.USE_BIG_DECIMAL_FOR_FLOATS)
    .serializationInclusion(JsonInclude.Include.NON_NULL)
    .build();
```
Add `ParameterNamesModule` (or compile with `-parameters`) for constructor binding; records work from Jackson 2.12+.

## Policies to decide deliberately
- **Unknown properties:** tolerant readers survive additive API changes; strict mode catches typos on inbound config files. Choose per mapper (`@JsonIgnoreProperties(ignoreUnknown = true)` per class).
- **Naming:** `PropertyNamingStrategies.SNAKE_CASE` globally or `@JsonProperty` per field.
- **Money/decimals:** serialize BigDecimal as string when clients are JavaScript (`@JsonFormat(shape = STRING)`), since JS numbers lose precision beyond 2^53.
- **Enums:** `READ_UNKNOWN_ENUM_VALUES_USING_DEFAULT_VALUE` with `@JsonEnumDefaultValue` for forward compatibility.
- **Max sizes (2.15+):** `StreamReadConstraints` limits nesting depth (1000), string length (20,000,000 chars default since 2.15/2.16), and number length to prevent DoS; raise only knowingly.

## Gotchas
- `new ObjectMapper()` per call is slow (serializer caches live in the mapper).
- Default typing (`enableDefaultTyping`/`activateDefaultTyping`) on untrusted JSON enables gadget-class deserialization attacks; use explicit subtype allow-lists (see `jackson-polymorphic-types-with-jsontypeinfo`).
- Mutating a mapper after first use is not thread-safe.
- Date-only fields: use `LocalDate`, not `Date`.
- Lombok `@Value`/records with a single-arg constructor can be ambiguous (delegating vs properties mode): annotate with `@JsonCreator(mode = PROPERTIES)`.

## Verify
Round-trip tests for `Instant`, `LocalDate`, `BigDecimal`, a record, an unknown field and a missing optional field; assert the exact JSON string output.

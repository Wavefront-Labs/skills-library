---
id: computing-software.software-engineering.java.jackson-polymorphic-types-with-jsontypeinfo
name: jackson-polymorphic-types-with-jsontypeinfo
category: computing-software
field: software-engineering
product: java
tags: [java, java-json, jackson-polymorphism, jsontypeinfo, jsonsubtypes, polymorphic-deserialization, default-typing]
level: advanced
status: docs-checked
description: "Serialize and deserialize class hierarchies with Jackson @JsonTypeInfo and @JsonSubTypes using logical type names, and avoid class-name type ids on untrusted input."
sources: ["https://github.com/FasterXML/jackson-annotations/wiki/Jackson-Annotations", "https://github.com/FasterXML/jackson-docs/wiki/JacksonPolymorphicDeserialization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jackson polymorphic types

## Explicit logical names (recommended)
```java
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = Card.class, name = "card"),
    @JsonSubTypes.Type(value = Transfer.class, name = "transfer")
})
public abstract class Payment {}

public class Card extends Payment { public String number; }
public class Transfer extends Payment { public String iban; }
```
JSON: `{"type":"card","number":"..."}`. The type id lives in a property named by `property`. Without `@JsonSubTypes` the deserializer cannot locate the subtypes when logical names are used.

Choices on `@JsonTypeInfo`:
- `use`: `CLASS` (fully-qualified class name), `MINIMAL_CLASS` (relative class name), `NAME` (logical name), `CUSTOM` (your own resolver via `@JsonTypeIdResolver`).
- `include`: `PROPERTY` (type id as a regular property), `WRAPPER_OBJECT` (type id is the field name of a wrapper object), `WRAPPER_ARRAY` (type id is the first array element).
- Names come from `@JsonTypeName` on the subtype or the `name` in the `@JsonSubTypes.Type` entry; if both exist the `@JsonSubTypes` one wins.
- `@JsonTypeId` marks a property whose value is the type id.

Logical names also keep the JSON usable by non-Java clients and decouple it from class names; the project's own design notes say class-name ids make integration with non-Java systems difficult.

## Security
Class-name type ids plus untrusted input expose deserialization gadgets: the attacker names any class reachable through the class loader. Jackson ships a block list of known gadgets, but new ones are found over time, so the wiki recommends against default typing for untrusted content. Default typing is acceptable when sender and receiver are controlled by the same entity.
```java
PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator.builder().build();
objectMapper.activateDefaultTyping(ptv, ObjectMapper.DefaultTyping.NON_FINAL);
```
`activateDefaultTyping` takes a `PolymorphicTypeValidator`; `DefaultTyping` choices are `JAVA_LANG_OBJECT`, `OBJECT_AND_NON_CONCRETE` (the default), `NON_CONCRETE_AND_ARRAYS` and `NON_FINAL`. Prefer `Id.NAME` with a closed `@JsonSubTypes` list over any of this.

## Gotchas
- A per-class `@JsonTypeInfo` overrides the global default typing.
- Renaming a subtype class is a breaking change for class-name ids; explicit `NAME` ids are stable.

## Verify
Round-trip every subtype in a parameterised test; add a case with an unknown `type` and assert a clear 400-level error rather than a stack trace to the client.

## Checked

Date: 2026-11-08

Read in full: the Jackson Polymorphic Deserialization wiki page and the Jackson Annotations wiki page. Confirmed: the `use` and `include` choices, `property`, `@JsonSubTypes`/`@JsonTypeName` precedence, `@JsonTypeId`, default typing modes and the validator parameter, and the gadget warning. Removed because neither page states them: `EXISTING_PROPERTY`, `DEDUCTION`, `defaultImpl`, the exception type for unknown ids, `registerSubtypes`/mixins, sealed interface and record support, the `allowIfSubType` snippet, list-erasure advice, and the OWASP cheat sheet source (not read).

Method: documentation only; no commands were run.

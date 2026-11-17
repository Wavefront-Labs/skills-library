---
id: computing-software.software-engineering.quarkus.quarkus-rest-json-native-reflection
name: quarkus-rest-json-native-reflection
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, rest, json, native-image, reflection, jackson]
level: practitioner
status: docs-checked
description: "Fix empty JSON from Quarkus REST in native builds: why Response hides the entity type, and the fixes (@RegisterForReflection, RestResponse), plus Jackson mapper tuning."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/rest-json.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON in Quarkus REST: native reflection and mapper tuning

## Setup

Add `quarkus-rest-jackson` (Jackson) or `quarkus-rest-jsonb` (JSON-B). With either, `application/json` is the default media type for most return values unless `@Produces`/`@Consumes` say otherwise (`String` stays `text/plain`, `File` stays `application/octet-stream`). Beans need a default constructor for the serialization layer.

## The native-image trap

JSON libraries use reflection; in a GraalVM native executable, classes must be registered for it. Quarkus infers serialized types at build time from REST method signatures, e.g. `public List<Fruit> list()`. It cannot do that when you return `jakarta.ws.rs.core.Response`, since the entity type is not visible:

```java
@GET
public Response list() { return Response.ok(legumes).build(); }
```

Symptom: works in JVM mode, but the native executable returns no fields. Neither Jackson nor JSON-B throws; GraalVM just returns an empty field list.

Fixes:

1. Annotate the entity with `io.quarkus.runtime.annotations.RegisterForReflection`.
2. Or return `org.jboss.resteasy.reactive.RestResponse<T>`; being strongly typed, Quarkus finds the type at build time and registers it automatically.

## Jackson defaults and customization

- Unknown properties are ignored (`FAIL_ON_UNKNOWN_PROPERTIES` disabled). Restore with `quarkus.jackson.fail-on-unknown-properties=true` or per class `@JsonIgnoreProperties(ignoreUnknown = false)`.
- Dates are written as ISO-8601 (`WRITE_DATES_AS_TIMESTAMPS` disabled). Restore with `quarkus.jackson.write-dates-as-timestamps=true`, or use `@JsonFormat` on one field.
- Preferred customization: a CDI bean implementing `io.quarkus.jackson.JsonMapperBuilderCustomizer` with `customize(JsonMapper.Builder builder)`.
- If you produce your own `JsonMapper` bean, inject all `JsonMapperBuilderCustomizer` beans (`@All List<...>`) and apply them yourself, otherwise extension customizations are lost.
- Mixins: annotate the mixin class with `io.quarkus.jackson.JacksonMixin`, naming the target class as the value.
- JSON-B equivalent: a bean implementing `io.quarkus.jsonb.JsonbConfigCustomizer`; same rule if you provide your own `Jsonb`.

## Checked

2026-11-07. Matched against the text (with includes) of: rest-json.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

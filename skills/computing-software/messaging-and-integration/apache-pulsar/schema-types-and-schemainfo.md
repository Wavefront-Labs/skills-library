---
id: computing-software.messaging-and-integration.apache-pulsar.schema-types-and-schemainfo
name: schema-types-and-schemainfo
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [schema, schema-info, primitive-types, keyvalue-schema, struct-schema, avro, protobuf-native]
level: practitioner
status: docs-checked
description: "Understand Pulsar SchemaInfo fields, primitive and complex schema types, KeyValue INLINE vs SEPARATED encoding and the three ways to build a struct schema."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/schema-understand.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right schema type and know what Pulsar stores for it.

A schema is a `SchemaInfo` stored and enforced per topic; it cannot be stored at namespace or tenant level. Fields: `name` (string), `type` (determines serialization), `schema` (bytes of schema data), `properties` (user-defined string map). Example string schema: name `test-string-schema`, type `STRING`, empty schema, empty properties.

Primitive types: `BOOLEAN`, `INT8`, `INT16`, `INT32`, `INT64`, `FLOAT`, `DOUBLE`, `BYTES`, `STRING`, `TIMESTAMP` (`DATE`, `TIME`; milliseconds since the epoch as INT64), `INSTANT`, `LOCAL_DATE`, `LOCAL_TIME`, `LOCAL_DATE_TIME` (the last four are Java types only). Pulsar stores no schema data in SchemaInfo for primitives; some use `properties` for tunables (for example the string charset).

Complex types:
- `KeyValue`: a schema for both key and value, stored together as the key schema and value schema. Encoding is `INLINE` (key and value together in the payload) or `SEPARATED` (key stored as message key, value as payload).
- `Struct`: `AvroBaseStructSchema` (Avro-based, covering Avro, JSON and Protobuf-generated classes), `ProtobufNativeSchema` (protobuf native descriptor, native protobuf-v3 serialization), and `NativeAvroBytesSchema` (wraps a native Avro `org.apache.avro.Schema` and accepts a serialized Avro payload without validating it).
- Auto schema, for consuming without knowing the type.

Struct schemas can be built three ways: static (a predefined POJO in Java, struct in Go, or Avro/Protobuf-generated class), generic, or `SchemaDefinition`. For a static Java class Pulsar derives the schema via an Avro library, for example `client.newProducer(Schema.AVRO(User.class))`.

Gotcha: the Java POJO needs a no-argument constructor (with Lombok use `@NoArgsConstructor`).

Verify: produce with a struct schema, then read the schema back with the admin schema commands and compare name and type.

## Checked

2026-11-03. Confirmed against the Pulsar schema understanding page: SchemaInfo fields, primitive type list and Java-only types, no stored schema data for primitives (charset in `properties`), KeyValue INLINE and SEPARATED encodings, struct schema classes, static/generic/`SchemaDefinition` construction, and the `@NoArgsConstructor` note.

Method: documentation only; no commands were run.

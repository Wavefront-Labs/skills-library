---
id: computing-software.data-engineering.apache-kafka.schema-references
name: schema-references
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, schema-registry, schema-references, avro, protobuf, json-schema, shared-types]
level: advanced
status: docs-checked
description: "Share types across Kafka schemas with Schema Registry references: registering referenced subjects first, Avro/Protobuf/JSON Schema syntax, versions and multi-event topics."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html#schema-references
  - https://docs.confluent.io/platform/current/schema-registry/develop/api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema references and shared types

A schema can reference other registered schemas (Confluent Schema Registry 5.5+), so a common `Address` or `Money` type is defined once, and one topic can carry several event types (`TopicRecordNameStrategy` or a union of references).

## Register the referenced schema first
```bash
curl -s -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"schemaType":"AVRO","schema":"{\"type\":\"record\",\"name\":\"Money\",\"namespace\":\"com.acme\",\"fields\":[{\"name\":\"amount\",\"type\":\"string\"},{\"name\":\"currency\",\"type\":\"string\"}]}"}' \
  $SR/subjects/com.acme.Money/versions
```
## Then the referencing schema
```bash
curl -s -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data @- $SR/subjects/orders-value/versions <<'JSON'
{"schemaType":"AVRO",
 "schema":"{\"type\":\"record\",\"name\":\"Order\",\"namespace\":\"com.acme\",\"fields\":[{\"name\":\"id\",\"type\":\"string\"},{\"name\":\"total\",\"type\":\"com.acme.Money\"}]}",
 "references":[{"name":"com.acme.Money","subject":"com.acme.Money","version":1}]}
JSON
```
- `name`: for Avro the fully qualified type name; for Protobuf the import path (`"acme/money.proto"`); for JSON Schema the `$ref` URL.
- References pin a **version**. Evolving `Money` means registering Money v2 and then a new version of each referencing schema pointing to v2.
- `GET /subjects/com.acme.Money/versions/1/referencedby` returns the IDs of schemas that reference that subject version; check it before deleting.

## Multiple event types in one topic (Avro)
Top-level union of references:
```json
{"schema":"[\"com.acme.OrderCreated\",\"com.acme.OrderCancelled\"]",
 "references":[{"name":"com.acme.OrderCreated","subject":"com.acme.OrderCreated","version":1},
               {"name":"com.acme.OrderCancelled","subject":"com.acme.OrderCancelled","version":1}]}
```
Schema references let several event types share one topic while keeping the subject-topic constraint; see the Confluent serializer docs for the producer settings that make the serializer use the union schema.

## Build tooling
- The Schema Registry Maven plugin can register schemas; register referenced schemas before the schemas that reference them.
- Protobuf: the serializer auto-registers imports as references when auto-register is on (`reference.subject.name.strategy`).

## Verify
- [ ] `GET $SR/subjects/orders-value/versions/latest` shows the `references` array.
- [ ] Consumers in each language deserialise a record using the referenced type.

## Checked
2026-11-01. Confirmed against Confluent's serializer and deserializer page (schema references): support from Platform 5.5.0, Avro/Protobuf/JSON Schema formats, register referenced schemas first, `referencedby` endpoint, Protobuf auto-registered references and `reference.subject.name.strategy`, multiple event types per topic. Removed: delete-blocking rule, producer config and ordering claims, and Maven `<references>` detail, which were not confirmed.
Method: documentation only; no commands were run.

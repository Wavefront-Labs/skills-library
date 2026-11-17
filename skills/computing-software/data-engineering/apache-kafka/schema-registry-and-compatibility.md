---
id: computing-software.data-engineering.apache-kafka.schema-registry-and-compatibility
name: schema-registry-and-compatibility
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, schema-registry, confluent-schema-registry, avro, protobuf, json-schema, backward-compatibility, forward-compatibility, full-compatibility, schema-evolution, serde, subject-naming-strategy]
level: practitioner
status: docs-checked
description: "Use Confluent Schema Registry compatibility modes and subject naming strategies to evolve topic schemas without breaking consumers."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema Registry and safe schema evolution

**Goal:** change a producer's message shape without the deploy breaking every consumer that hasn't updated yet.

## 1. What Schema Registry actually does
Producers using the registry-aware serializer register (or look up) the schema for a topic and get back a schema ID; the serialized message carries a magic byte and the schema ID ahead of the payload, not the schema itself. Consumers use the ID to fetch the schema and deserialize. Registry-side compatibility rules gate *registration*, so a producer trying to register an incompatible schema fails at registration rather than writing a message consumers cannot read.

## 2. Compatibility modes — pick one per subject and mean it
Set per-subject (usually `<topic>-value`), not just globally:
- **BACKWARD**: new schema can read data written with the previous schema. Allows deleting a field, or adding a field *with a default*. Consumers must upgrade before producers can safely remove fields they still rely on, but new consumers can read old data.
- **FORWARD**: old schema can read data written with the new schema. Allows adding a field, or deleting a field that had a default. Lets producers deploy first, before consumers.
- **FULL**: both — the intersection, safest, most restrictive (usually: add/remove only fields with defaults).
- **_TRANSITIVE** variants check against *all* previous versions, not just the immediately prior one — use when a topic has had many revisions and you need to guarantee compatibility across the whole history, not just a one-step hop.
- **NONE**: no checks. Only acceptable for throwaway/dev topics.
- **Renaming a field** needs care: the Confluent schema evolution page discusses renames and Avro aliases; read it before renaming rather than treating a rename as a plain edit.

## 3. Subject naming and multi-type topics
Default **TopicNameStrategy** gives one subject (hence one schema lineage) per topic — breaks if a topic legitimately carries multiple record types. **RecordNameStrategy** keys the subject on the record's fully-qualified name instead, letting one topic carry multiple schemas safely; **TopicRecordNameStrategy** combines both when you want per-topic-per-type lineage. Decide this before topics are in production.

## Verify
- [ ] Subject-level compatibility mode is set explicitly (not left at the registry's global default) and matches the actual rollout order (producer-first vs consumer-first).
- [ ] A schema change that violates compatibility fails in a pre-deploy check, not in production.
- [ ] Every new field added has a default value.

## Checked
2026-11-01. Confirmed against the Confluent Platform pages Schema Evolution and Compatibility (BACKWARD, FORWARD, FULL and TRANSITIVE modes, renames and aliases) and Formats, Serializers, and Deserializers (magic byte and schema ID, TopicNameStrategy, RecordNameStrategy, TopicRecordNameStrategy). Removed: Apicurio, the Avro/Protobuf/JSON Schema comparison and Protobuf version claim, the CI plugin claim and the claim that BACKWARD is the most common default.
Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.apache-kafka.choosing-serializers
name: choosing-serializers
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-serializers, serdes, avro, protobuf, json-schema, schema-registry, kafka-producer]
level: practitioner
status: docs-checked
description: "Choose Kafka key and value serializers (string, JSON, Avro, Protobuf, JSON Schema) and wire Schema Registry serdes, with key-format rules that affect partitioning."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing serializers and serdes

## Options
| Format | Serializer | Pros | Cons |
|---|---|---|---|
| String/bytes | `StringSerializer`, `ByteArraySerializer` | simple, any tool reads it | no contract |
| JSON (schemaless) | your own serializer | human-readable | verbose, no enforced schema, type drift |
| Avro + Schema Registry | `io.confluent.kafka.serializers.KafkaAvroSerializer` | compact, strong evolution rules | needs registry; not human-readable |
| Protobuf + SR | `KafkaProtobufSerializer` | compact, good for polyglot services already using proto | evolution rules differ from Avro |
| JSON Schema + SR | `KafkaJsonSchemaSerializer` | readable plus validation | larger payloads |

## Wiring (Java)
```properties
key.serializer=org.apache.kafka.common.serialization.StringSerializer
value.serializer=io.confluent.kafka.serializers.KafkaAvroSerializer
schema.registry.url=https://sr:8081
auto.register.schemas=false        # register via CI, not from production producers
use.latest.version=true
```
SR serializers prepend a header (a magic byte, then a 4-byte schema ID); consumers must use the matching deserializer, or they see garbage leading bytes.

## Keys deserve special care
- The key's **serialized bytes** decide the partition. Changing key format (String to Avro, or adding a field) moves keys to different partitions and breaks ordering and compaction.
- Keep keys as plain strings or primitives unless there is a strong reason; Avro keys embed a schema id, so a new key schema version changes the bytes for the same logical key.
- Compacted topics and Kafka Streams joins require byte-identical keys for the same entity.

## Verify
- [ ] Consumers in every language deserialise a sample record.
- [ ] Key bytes for the same entity are identical across producers (hash check in a test).

## Checked
2026-11-01. Confirmed against Confluent's serializer and deserializer page: the Avro, Protobuf and JSON Schema serializer class names, the wire format (magic byte then 4-byte schema ID), and `auto.register.schemas` / `use.latest.version` behaviour. Removed: Spring and Python client claims, ecosystem pros and cons, and the hash algorithm name, which were not confirmed.
Method: documentation only; no commands were run.

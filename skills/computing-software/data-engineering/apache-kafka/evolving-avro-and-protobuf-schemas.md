---
id: computing-software.data-engineering.apache-kafka.evolving-avro-and-protobuf-schemas
name: evolving-avro-and-protobuf-schemas
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, schema-registry, avro-schema-evolution, protobuf-evolution, backward-compatibility, default-values, field-numbers, schema-changes]
level: practitioner
status: docs-checked
description: "Make safe schema changes in Avro and Protobuf on Kafka: which edits are backward/forward compatible, defaults, field numbers, renames via aliases, and upgrade order."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
  - https://avro.apache.org/docs/1.11.1/specification/#schema-resolution
  - https://protobuf.dev/programming-guides/proto3/#updating
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evolving Avro and Protobuf schemas

**Goal:** change event schemas without breaking running consumers, picking the edit and deploy order that the subject's compatibility mode allows.

## Compatibility -> who upgrades first
| Mode | Guarantee | Deploy order |
|---|---|---|
| BACKWARD (default) | new schema can read old data | consumers first, then producers |
| FORWARD | old schema can read new data | producers first |
| FULL | both | any order |
| *_TRANSITIVE | against all previous versions, not just latest | same as the non-transitive mode |

## Avro edit cheat-sheet
| Change | BACKWARD | FORWARD |
|---|---|---|
| Add field **with default** | ok | ok |
| Add field without default | breaks | ok |
| Remove field with default | ok | ok |
| Remove field without default | ok | breaks |
| Widen a scalar type (Avro promotions: int to long/float/double, long to float/double, float to double, string and bytes) | ok | breaks |

Renaming: the Avro spec lets a reader schema list `aliases` to map a writer's field or type names onto its own.

```json
{"name": "discount_code", "type": ["null", "string"], "default": null}
```

## Protobuf rules
- Never reuse or change a field **number**; field numbers 19,000 to 19,999 are reserved for the Protobuf implementation.
- Adding or removing optional fields is compatible in all Schema Registry modes.
- Narrowing an integer (for example `int64` to `int32`) is wire-compatible but readers silently truncate values that do not fit; Schema Registry's LOGICAL policy rejects it.
- Adding a new message type (union/oneof variant) is not forward compatible, so the Confluent best practice for Protobuf is BACKWARD_TRANSITIVE.

## Process
1. Edit schema; run the compatibility check locally/CI:
```bash
curl -s -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data "{\"schema\": $(jq -Rs . < order.avsc)}" \
  $SR/compatibility/subjects/orders-value/versions/latest | jq .is_compatible
```
2. Deploy in the order dictated by the mode.
3. Breaking change needed? Create a new topic/subject (`orders.v2`), dual-publish, migrate consumers.

## Gotchas
- Producers with `auto.register.schemas=true` register whatever they compile with; consider disabling it in prod and registering from CI.
- A default value only helps readers; writers must still populate the field.

## Verify
- [ ] CI compatibility check passes against latest (or all, for transitive).
- [ ] Old consumer binary can read records produced with the new schema in a staging test.

## Checked
2026-11-01. Confirmed against Confluent's Schema Evolution and Compatibility page (default BACKWARD, mode definitions, upgrade order, allowed-change table, Protobuf best practice, narrowing-integer truncation), the Avro specification (promotions, aliases) and the proto3 guide (reserved field number range). Removed: enum symbol and nullable rows, union default rule, Protobuf reserved syntax and rename claims, and logical type claim, which were not confirmed.
Method: documentation only; no commands were run.

---
id: computing-software.messaging-and-integration.apache-pulsar.schema-compatibility-and-autoupdate
name: schema-compatibility-and-autoupdate
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [schema-compatibility, backward, forward, full, transitive, schema-autoupdate, schema-validation]
level: advanced
status: docs-checked
description: "Choose and set a Pulsar schema compatibility strategy (BACKWARD, FORWARD, FULL, transitive, ALWAYS_*), defaults by type, AutoUpdate rules and client upgrade order."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/schema-understand.md
  - https://github.com/apache/pulsar-site/blob/main/docs/admin-api-schemas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let schemas evolve without breaking existing producers or consumers.

When a producer or consumer connects with a `SchemaInfo`, the broker uses the checker for that schema type from `schemaRegistryCompatibilityCheckers` in broker.conf. Each type gets one checker; they do not chain. For `PROTOBUF_NATIVE` the default checker compares root message names only.

Eight strategies (V1 oldest, V3 newest):
- `ALWAYS_COMPATIBLE`: no check; any change.
- `ALWAYS_INCOMPATIBLE`: schema evolution disabled; no change allowed.
- `BACKWARD`: consumers on V3 read data from the last version V2. Allowed: add optional fields, delete fields. Checked against the latest version.
- `BACKWARD_TRANSITIVE`: same but against all previous versions.
- `FORWARD`: consumers on the last version read data from new V3. Allowed: add fields, delete optional fields. Latest version.
- `FORWARD_TRANSITIVE`: against all previous versions.
- `FULL`: backward and forward with the last version; `FULL_TRANSITIVE`: across all versions.

Defaults: `FULL` for Avro and JSON; `ALWAYS_INCOMPATIBLE` for other types.

Where to set it (priority topic over namespace over cluster):
```shell
pulsar-admin topicPolicies set-schema-compatibility-strategy <strategy> <topicName>
pulsar-admin namespaces set-schema-compatibility-strategy options
```
Cluster level: `schemaCompatibilityStrategy` in broker.conf.

AutoUpdate is enabled by default: a compatible schema is registered automatically by the producer. If the topic has no schema, Pulsar registers the producer's schema. If the topic has a schema and the producer sends raw bytes, it is accepted only when `schemaValidationEnforced=false` in the namespace. Consumers on a schema-less topic connect without a check. If AutoUpdate is not allowed and the schema is unregistered, the broker rejects the producer.

Upgrade order depends on strategy: no order for `ALWAYS_COMPATIBLE`; for `BACKWARD` and `BACKWARD_TRANSITIVE` upgrade consumers first.

## Checked

2026-11-03. Confirmed against the Pulsar schema understanding and schema admin API pages: `schemaRegistryCompatibilityCheckers` (one checker per type, no chain, PROTOBUF_NATIVE compares root message names), the strategy table, defaults (FULL for Avro and JSON, ALWAYS_INCOMPATIBLE otherwise), topic over namespace over cluster priority, both set-schema-compatibility-strategy commands, `schemaCompatibilityStrategy`, `schemaValidationEnforced=false` behaviour and upgrade order. Removed: the generic Verify line.

Method: documentation only; no commands were run.

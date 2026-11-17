---
id: computing-software.messaging-and-integration.redpanda.schema-registry-api-register-and-retrieve
name: schema-registry-api-register-and-retrieve
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [schema-registry, avro, protobuf, subjects, rpk-registry, rest-api]
level: practitioner
status: docs-checked
description: "Register Avro and Protobuf schemas in Redpanda Schema Registry with rpk or curl, list subjects and versions, and prefer pre-registering schemas over client auto-registration."
sources:
  - https://docs.redpanda.com/streaming/current/manage/schema-reg/schema-reg-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Schema Registry is built into Redpanda; the examples assume it is at `http://localhost:8081`. `rpk registry` commands call the same endpoints as curl.

- Supported formats: `GET /schemas/types` returns `JSON`, `PROTOBUF` and `AVRO`.
- A schema is registered under a **subject**, typically `<topic-name>-key` or `<topic-name>-value`. POST to `/subjects/<subject>/versions` with Content-Type `application/vnd.schemaregistry.v1+json`; add `?normalize=true` to normalize.

```bash
rpk registry schema create sensor-value --schema ~/code/tmp/sensor_sample.avro
rpk registry schema create sensor-proto-value --schema sensor_sample.proto
```

Retrieval and listing:

```bash
rpk registry schema get --id 1
rpk registry subject list --format json
rpk registry schema get sensor-value --schema-version 1
rpk registry schema get sensor-value --schema-version latest
```

**Pre-register in shared and production environments.** Confluent-compatible serializers auto-register by default. Instead, register at topic-creation time with `rpk registry schema create` or `POST /subjects/{subject}/versions`, and configure clients to look schemas up. Registration needs the `write` operation on the `subject` resource when Schema Registry ACLs are enforced, and auto-registration also fails when the subject is in READONLY or IMPORT mode.

Cross-references use `--references`, for example `rpk registry schema create import --schema import_schema.proto --references simple:test-simple:2`; check dependents with `rpk registry schema references test-simple --schema-version 1`. A schema referenced by another cannot be deleted.

## Checked

2026-11-04. Commands, subject naming, supported formats, pre-registration guidance and reference deletion limits were confirmed on the Schema Registry API page.

Method: documentation only; no commands were run.

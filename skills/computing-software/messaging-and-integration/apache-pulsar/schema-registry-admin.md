---
id: computing-software.messaging-and-integration.apache-pulsar.schema-registry-admin
name: schema-registry-admin
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [schema-registry, schemas-upload, schemas-get, schemas-delete, schema-payload, producer-schema]
level: practitioner
status: docs-checked
description: "Manage Pulsar topic schemas with pulsar-admin schemas upload/get/extract/delete, the JSON payload shape, REST endpoint and how producers and consumers register schemas."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/admin-api-schemas.md
  - https://github.com/apache/pulsar-site/blob/main/docs/schema-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: register, inspect and remove schemas on topics, and understand how clients trigger registration.

Concept: messages are stored as unstructured bytes; a schema is applied when reading and enforced per topic. The schema registry is stored in BookKeeper and brokers coordinate it. Producers and consumers upload schemas by connecting with a schema instance, for example `client.newProducer(JSONSchema.of(User.class)).topic(topic).create()`. The broker returns the schema version if registered; otherwise it checks auto-update and runs the compatibility check, rejecting the client on failure. Messages are tagged with the schema version.

Admin commands:
```bash
pulsar-admin schemas upload --filename <schema-definition-file> <topic-name>
pulsar-admin schemas get <topic-name>
pulsar-admin schemas get <topic-name> --version <version>
pulsar-admin schemas extract --classname <class-name> --jar <absolute-jar-path> --type <type-name>
pulsar-admin schemas delete <topic-name>
```
Definition file (JSON): `{"type": "<schema-type>", "schema": "<utf8 string of schema definition>", "properties": {}}`.

REST upload: `curl -X POST -H 'Content-Type: application/json' -d @schema.json http://localhost:8080/admin/v2/schemas/my-tenant/my-ns/my-topic/schema`. Java admin: `admin.createSchema(topic, payload)` with a `PostSchemaPayload` (`setType`, `setSchema`).

Payload rules: for a primitive schema the `schema` field must be blank. For AVRO, PROTOBUF and JSON it must be an Avro schema definition in JSON format; for PROTOBUF_NATIVE it must contain a Protobuf descriptor. The `schema` data is UTF-8 encoded. Struct `type` values are AVRO, PROTOBUF, PROTOBUF_NATIVE and JSON; primitive values are those in the primitive type list.

Gotcha: a topic that is already in use must have a compatible schema, so uploading an incompatible definition fails the compatibility check rather than replacing the old one.

Verify: upload a schema, then `schemas get` it and compare type and definition.

## Checked

2026-11-03. Confirmed against the Pulsar schema admin API and schema overview pages: the `schemas upload|get|extract|delete` commands and flags, REST upload, `createSchema` with `PostSchemaPayload`, primitive-schema blank `schema` field, BookKeeper storage. Fixed: PROTOBUF_NATIVE takes a Protobuf descriptor, not an Avro definition.

Method: documentation only; no commands were run.

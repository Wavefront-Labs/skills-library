---
id: computing-software.messaging-and-integration.apache-pulsar.debezium-source-connector
name: debezium-source-connector
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [debezium, cdc, source-connector, database-history, offset-storage-topic, json-with-envelope]
level: practitioner
status: docs-checked
description: "Configure the Pulsar IO Debezium source for MySQL, PostgreSQL or MongoDB: required properties, history and offset topics, converter choice and reader config."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/io-debezium-source.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stream change-data-capture events from a database into Pulsar topics.

The Debezium source pulls messages from MySQL or PostgreSQL (MongoDB properties are separate) and persists them to Pulsar. Download the connector from the Pulsar download page.

Required relational properties: `task.class` (a Debezium source task class), `database.hostname`, `database.port`, `database.user`, `database.password`, `database.server.id` (unique within the database cluster, like the database server-id), `topic.prefix` (logical server name used as the namespace for topic and schema names), `key.converter`, `value.converter`, `database.history` (history class name), `database.history.pulsar.topic` (internal topic that stores DDL statements; consumers must not use it), `offset.storage.topic` (records last committed offsets).

Optional: `database.include.list` (databases to monitor), `database.history.pulsar.service.url` (if unset the history client uses the connector's own Pulsar client settings), `json-with-envelope` (default false), `database.history.pulsar.reader.config` and `offset.storage.reader.config` (JSON strings of reader settings).

MongoDB: `mongodb.hosts`, `mongodb.name` (unique name for the replica set or cluster; each server should be monitored by at most one Debezium connector), `mongodb.user` and `mongodb.password` (only when authentication is on), `mongodb.task.id`.

Converters:
- `org.apache.kafka.connect.json.JsonConverter`: with `json-with-envelope=false` consume with `Schema.KeyValue(Schema.AUTO_CONSUME(), Schema.AUTO_CONSUME(), KeyValueEncodingType.SEPARATED)`. With `true` use `Schema.KeyValue(Schema.BYTES, Schema.BYTES)` and the message carries schema plus payload. `json-with-envelope` is valid only for JsonConverter.
- `org.apache.pulsar.kafka.shade.io.confluent.connect.avro.AvroConverter`: consume with the same AUTO_CONSUME key-value schema, payload only.

Reader config example (YAML): `database.history.pulsar.reader.config: "{\"subscriptionName\":\"history-reader\"}"` and `offset.storage.reader.config: "{\"subscriptionName\":\"offset-reader\"}"`.

Gotcha: pick the consumer schema to match the converter, or messages will not decode.

Verify: change a row and consume the resulting event from the table topic under `topic.prefix`.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/io-debezium-source.md (configuration, converter and MongoDB sections read)

---
id: computing-software.messaging-and-integration.debezium.mysql-schema-history-topic
name: mysql-schema-history-topic
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, schema-history, ddl, kafka-topic]
level: advanced
status: docs-checked
description: "How the internal MySQL schema history topic rebuilds table structure on restart, and the properties that configure it."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The binlog holds row changes and DDL. The connector parses DDL as it reads, keeps an in-memory table schema, and records every DDL statement with its binlog position in a Kafka schema history topic. On restart it rebuilds table structures by replaying that topic up to the starting position.

Configure it with:

```json
"schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
"schema.history.internal.kafka.topic": "schema-changes.inventory"
```

The topic is for internal connector use only; consumers must not read it. The connector rebuilds table structures from it on restart, so keep it; its configuration requirements are in the Debezium installation documentation.

Related properties:

- `schema.history.internal.store.only.captured.tables.ddl` (default `false`): by default the snapshot records schema for all non-system tables, including ones not captured. Set `true` to store only captured tables and shrink the topic. If a captured table's schema is missing from the history topic, the connector fails to capture it and reports a missing schema error.
- `schema.history.internal.skip.unparseable.ddl` (default `false`): `true` ignores malformed or unknown statements, but can cause data loss or mangled events. Use with care.

Gotcha: tools such as gh-ost and pt-online-schema-change create helper tables during migrations. The connector must capture changes in those tables; if consumers do not need them, drop their records with an SMT.

Check: after the first snapshot, confirm the history topic exists and has records.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: how the history topic rebuilds table structure, the two schema.history.internal.kafka properties, internal-use-only, store.only.captured.tables.ddl and skip.unparseable.ddl, gh-ost and pt-online-schema-change helper tables.
Removed or reworded: the indefinite-retention and no-compaction claim, the 'do this only when' advice (replaced by the documented failure).
Method: documentation only; no commands were run.

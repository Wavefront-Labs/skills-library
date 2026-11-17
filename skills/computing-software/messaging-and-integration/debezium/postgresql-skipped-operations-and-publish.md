---
id: computing-software.messaging-and-integration.debezium.postgresql-skipped-operations-and-publish
name: postgresql-skipped-operations-and-publish
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, skipped-operations, filtering, publication]
level: practitioner
status: docs-checked
description: "Skip create, update, delete or truncate events on the PostgreSQL connector, and how pgoutput publish options reflect it."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`skipped.operations` takes a comma-separated list of operation types the connector ignores during streaming:

- `c` insert/create
- `u` update
- `d` delete
- `t` truncate
- `none` to skip nothing

The connector default is `t`, so truncates are skipped unless you change it. Set `none` to receive them.

With the `pgoutput` plug-in and `publication.autocreate.mode` set to `all_tables` or `filtered`, the connector writes your choice into the publication. For example `skipped.operations=d` creates or updates the publication with `WITH (publish = 'insert,update,truncate')`. PostgreSQL then omits deletes from the stream at the source, which reduces WAL traffic to the connector.

```json
"skipped.operations": "d,t"
```

Related event behaviour: `tombstones.on.delete` (default `true`) emits a tombstone after each delete event so Kafka log compaction can remove the key. Set it to `false` if you only want the delete event.

Gotcha: skipped deletes mean downstream copies never remove rows. Choose this only for append-only consumers.

Gotcha: if a publication already exists, the connector uses it as defined, so set its `publish` options yourself.

Check: after changing the setting, inspect the publication's publish options in PostgreSQL.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: skipped.operations values and default, the publish clause for pgoutput, tombstones.on.delete.
Removed or reworded: the pg_publication query.
Method: documentation only; no commands were run.

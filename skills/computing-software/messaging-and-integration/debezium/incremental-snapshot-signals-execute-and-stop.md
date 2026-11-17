---
id: computing-software.messaging-and-integration.debezium.incremental-snapshot-signals-execute-and-stop
name: incremental-snapshot-signals-execute-and-stop
category: computing-software
field: messaging-and-integration
product: debezium
tags: [signaling, incremental-snapshot, execute-snapshot, stop-snapshot]
level: advanced
status: docs-checked
description: "Trigger and stop ad hoc incremental snapshots with execute-snapshot and stop-snapshot signals, including additional-conditions filters."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: signaling is enabled, the signal table exists, and `signal.data.collection` points to it.

Start a snapshot with an `INSERT` into the signal table:

```sql
INSERT INTO myschema.debezium_signal (id, type, data)
values ('ad-hoc-1', 'execute-snapshot',
 '{"data-collections": ["schema1.table1", "schema1.table2"],
 "type":"incremental",
 "additional-conditions":[{"data-collection": "schema1.table1", "filter":"color=''blue''"}]}');
```

Rules:

- `data-collections` is an array of names or regular expressions; names are case-sensitive and have no default. An empty array means no snapshot runs.
- Names containing a dot, space or other non-alphanumeric character must be escaped in double quotes, for example `"public.\"My.Table\""`.
- `type` is `incremental` (default) or `blocking`.
- `additional-conditions` takes a filter fragment appended to the query for incremental snapshots, such as `color='blue'`.
- The `id` is an arbitrary label that helps tell signal requests apart and match log messages to signal table rows; Debezium does not otherwise use it.

Stop a running snapshot:

```sql
INSERT INTO myschema.debezium_signal (id, type, data)
values ('ad-hoc-2', 'stop-snapshot', '{"data-collections": ["schema1.table1"], "type":"incremental"}');
```

`type` must be `incremental` or the signal fails. Omit `data-collections` to stop the whole snapshot.

Tuning: `incremental.snapshot.chunk.size` defaults to `1024` rows per chunk; bigger chunks mean fewer queries but more memory.

Use ad hoc snapshots after changing captured tables, rebuilding deleted topics, or fixing corrupted data. Output is appended to the existing topic.

## Checked

The signal fields, defaults, escaping rule, stop-snapshot behaviour, chunk size default and ad hoc snapshot use cases were confirmed on the PostgreSQL connector page. The page's own example writes the filter quote as a backslash-escaped single quote; the doubled single quote here is standard SQL string escaping and was not taken from the page.

Method: docs-checked 2026-11-09 against the debezium.io stable PostgreSQL connector page (read the ad hoc snapshot, stopping and chunk size sections of the downloaded HTML).

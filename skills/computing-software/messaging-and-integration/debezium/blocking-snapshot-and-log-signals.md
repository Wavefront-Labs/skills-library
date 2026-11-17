---
id: computing-software.messaging-and-integration.debezium.blocking-snapshot-and-log-signals
name: blocking-snapshot-and-log-signals
category: computing-software
field: messaging-and-integration
product: debezium
tags: [signaling, blocking-snapshot, log-signal, snapshot]
level: advanced
status: docs-checked
description: "Run a blocking snapshot on demand and use the log signal to print messages with streaming coordinates."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
  - https://debezium.io/documentation/reference/stable/configuration/signalling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A blocking snapshot captures a complete, consistent snapshot of a table at runtime. The connector stops streaming, snapshots the table like an initial snapshot, then resumes streaming. Choose it when you add a new table and want it done while the connector runs, or when a large table must finish faster than an incremental snapshot allows.

Send it as an `execute-snapshot` signal with `type` set to `blocking`:

```sql
INSERT INTO debezium_signal (id, type, data) VALUES ('blk-1', 'execute-snapshot',
 '{"type":"blocking","data-collections":["public.new_table"]}');
```

Options in `data`:

- `data-collections`: comma-separated names or regular expressions, behaving like `table.include.list`.
- `additional-conditions`: per-table filters. For blocking snapshots the `filter` must be a full `SELECT` statement, the same value you would put in `snapshot.select.statement.overrides`, and table names must match case.

Log signal: write a line to the connector log at a known position.

```
id: 924e3ff8-2245-43ca-ba77-2af9af02fa07
type: log
data: {"message": "Signal message at offset {}"}
```

A `{}` placeholder is replaced with the streaming coordinates, which helps you correlate a point in time with log positions.

Available actions per the docs: log, ad hoc incremental snapshot, stop snapshot, pause and resume incremental snapshots, blocking snapshot, and custom actions. Not every signal works on every connector.

Gotcha: unlike incremental snapshots, which keep streaming, a blocking snapshot stops streaming until it finishes.

## Checked

2026-11-08. Confirmed against the Debezium pages connectors/postgresql (read in part: Blocking snapshots and the ad hoc triggering section) and configuration/signalling (read in full: log signal, blocking snapshot, action list). Removed the log retention advice, which neither page states, and reworded the gotcha to what the pages say.

Method: documentation only; no commands were run.

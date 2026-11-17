---
id: computing-software.messaging-and-integration.debezium.postgresql-snapshot-modes
name: postgresql-snapshot-modes
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, snapshot, snapshot-mode, offsets]
level: practitioner
status: docs-checked
description: "Pick the right snapshot.mode for the PostgreSQL connector: initial, always, initial_only, no_data, when_needed, configuration_based or custom."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`snapshot.mode` (default `initial`) decides what happens at connector start.

- `initial`: snapshot only when no offsets exist for the logical server name.
- `always`: snapshot on every start, then stream.
- `initial_only`: snapshot, then stop without streaming.
- `no_data`: never snapshot. With a stored LSN it resumes there; with none it streams from when the slot was created. Use only if all data of interest is still in the WAL.
- `when_needed`: snapshot if no offsets exist or the recorded position is no longer available on the server.
- `configuration_based`: you set `snapshot.mode.configuration.based.snapshot.data`, `.snapshot.schema`, `.start.stream`, `.snapshot.on.schema.error` and `.snapshot.on.data.error`, all defaulting to `false`.
- `custom`: a class named by `snapshot.mode.custom.name` implementing `io.debezium.spi.snapshot.Snapshotter`.

Related tuning: `snapshot.isolation.mode` defaults to `serializable`, the most restrictive and safest; `snapshot.fetch.size` defaults to 10240 rows per batch; `snapshot.max.threads` defaults to 1 and, above 1, splits tables into primary-key chunks (tables without a primary key stay single-threaded).

Gotcha: `no_data` never snapshots, so use it only if all data of interest is still in the WAL.

Check: look in the connector log for the snapshot start and completion lines on first run.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: snapshot.mode values and defaults, configuration_based properties, custom Snapshotter, snapshot.isolation.mode, snapshot.fetch.size, snapshot.max.threads.
Removed or reworded: the incremental-snapshot advice.
Method: documentation only; no commands were run.

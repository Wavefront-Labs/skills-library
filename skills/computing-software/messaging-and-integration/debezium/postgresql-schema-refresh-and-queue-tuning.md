---
id: computing-software.messaging-and-integration.debezium.postgresql-schema-refresh-and-queue-tuning
name: postgresql-schema-refresh-and-queue-tuning
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, schema-refresh, performance, queue]
level: advanced
status: docs-checked
description: "Tune schema.refresh.mode, max.queue.size, max.batch.size and poll.interval.ms for the PostgreSQL connector."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Performance-related properties and their documented defaults:

- `schema.refresh.mode` (default `columns_diff`): the safest mode, keeps the in-memory schema in sync with the table. `columns_diff_exclude_unchanged_toast` skips refreshes when unchanged TOAST data explains the difference, which can speed up tables with big, rarely updated TOAST columns. The risk is a stale in-memory schema if TOASTable columns are dropped.
- `max.queue.size` (default `8192`): the blocking queue between the database reader and Kafka. It provides backpressure when Kafka is slow or down.
- `max.batch.size` (default `2048`): the largest batch processed. Always keep `max.queue.size` larger than this.
- `poll.interval.ms` (default `500`): wait per iteration for new changes; values above 5000 are capped at 5000.
- `snapshot.fetch.size` (default `10240`): rows per snapshot batch.

```json
"max.queue.size": "16384",
"max.batch.size": "4096",
"poll.interval.ms": "200"
```

Events held in the queue are disregarded when the connector periodically records offsets.

Plug-in note: `pgoutput` refreshes metadata more eagerly than other plug-ins, so a change to a column default triggers a refresh with `pgoutput` only.

Check: watch the streaming metrics for queue remaining capacity while load testing, and raise sizes in steps.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: schema.refresh.mode values and risk, max.queue.size, max.batch.size, poll.interval.ms cap, snapshot.fetch.size, pgoutput refresh note.
Removed or reworded: the re-read-after-crash inference.
Method: documentation only; no commands were run.

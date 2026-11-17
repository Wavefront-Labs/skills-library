---
id: computing-software.database-administration.clickhouse.cascading-materialized-views
name: cascading-materialized-views
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, cascading, materialized-view, null-engine, summingmergetree]
level: practitioner
status: docs-checked
description: "Chain materialized views from a Null-engine source table to build monthly and yearly rollups without storing raw rows."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/cascading-materialized-views.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cascading materialized views
When only aggregates matter, ingest into a `Null` table: it stores nothing, but materialized views attached to it still receive every inserted block.
```sql
CREATE TABLE analytics.hourly_data
( domain_name String, event_time DateTime, count_views UInt64 )
ENGINE = Null;
```
Attach a first view that aggregates to month into a SummingMergeTree target, then cascade a second view from that target to year. Each view writes to its own `TO` table or inner table, so the second reads from the output of the first.

Points to remember:
- Views fire on insert only, so they see new data, not history.
- A view runs on the inserted block, not the whole table, so aggregates must be mergeable (sum, count, `-State` functions with AggregatingMergeTree).
- Querying a SummingMergeTree target still needs `GROUP BY` and `sum()` because merges are eventual.

Gotcha: a Null table stores nothing, so the raw rows cannot be replayed.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Cascading materialized views": the Null-engine ingest table, month to year cascade into SummingMergeTree targets, and GROUP BY with sum on read. Removed: the backfill advice and the Verify step.
Method: documentation only; no commands were run.

---
id: computing-software.database-administration.clickhouse.incremental-materialized-views
name: incremental-materialized-views
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, materialized-view, summingmergetree, to-table, null-engine]
level: practitioner
status: docs-checked
description: "Build an incremental materialized view with a TO target table, SummingMergeTree rollups, Null source tables and insert-only JOIN triggers."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/materialized-view/incremental-materialized-view.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# incremental materialized views
A ClickHouse materialized view is an insert trigger: it runs its SELECT on each block of rows inserted into the source table and writes the result into a target table. It never re-reads existing data.

```sql
CREATE TABLE up_down_votes_per_day
(Day Date, UpVotes UInt32, DownVotes UInt32)
ENGINE = SummingMergeTree ORDER BY Day;

CREATE MATERIALIZED VIEW up_down_votes_per_day_mv TO up_down_votes_per_day AS
SELECT toStartOfDay(CreationDate)::Date AS Day,
       countIf(VoteTypeId = 2) AS UpVotes,
       countIf(VoteTypeId = 3) AS DownVotes
FROM votes GROUP BY Day;
```
Each insert block produces partial rows; the SummingMergeTree adds them at merge time, so queries should aggregate (`SELECT Day, sum(UpVotes) ... GROUP BY Day`) or use `FINAL`.

Variations from the docs:
- A source of ENGINE = Null (`CREATE TABLE posts_null AS posts ENGINE = Null`) lets the view compute summaries while the raw data is not stored.
- Percentiles and distinct counts need AggregatingMergeTree with `-State` functions and `-Merge` at read.
- JOINs: the view fires only on inserts into the left-most table; changes to right-side tables do not trigger updates, and JOINs increase insert cost, especially with large right-side tables.

## Checked
2026-11-03. Confirmed against the ClickHouse docs page "Incremental materialized view": trigger-on-inserted-blocks semantics, the SummingMergeTree example pattern, the Null engine option, JOIN left-most-table rule and insert cost. Removed: the backfill, drop-and-recreate and error-propagation gotchas and the Verify step, not stated in that form.
Method: documentation only; no commands were run.

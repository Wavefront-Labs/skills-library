---
id: computing-software.database-administration.clickhouse.aggregating-and-summing-mergetree
name: aggregating-and-summing-mergetree
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, summingmergetree, aggregatingmergetree, state, merge, materialized-view]
level: practitioner
status: docs-checked
description: "Pre-aggregate with SummingMergeTree and AggregatingMergeTree using -State and -Merge functions fed by materialized views."
sources:
  - https://clickhouse.com/docs/reference/engines/table-engines/mergetree-family/aggregatingmergetree
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/materialized-view/incremental-materialized-view.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# aggregating and summing mergetree
Merge-time engines let a target table hold partial aggregates that collapse during background merges.
```sql
CREATE TABLE hits_by_day (day Date, domain String, views UInt64)
ENGINE = SummingMergeTree ORDER BY (domain, day);

CREATE TABLE uniq_by_day (day Date, domain String, users AggregateFunction(uniq, UInt64))
ENGINE = AggregatingMergeTree ORDER BY (domain, day);

CREATE MATERIALIZED VIEW uniq_mv TO uniq_by_day AS
SELECT toDate(ts) AS day, domain, uniqState(user_id) AS users
FROM events GROUP BY day, domain;

SELECT day, domain, uniqMerge(users) FROM uniq_by_day GROUP BY day, domain;
```
Rules: SummingMergeTree sums numeric columns sharing an ORDER BY key; AggregatingMergeTree stores `-State` values read back with `-Merge`.

Gotcha: merges are eventual, so a query must still `GROUP BY` and aggregate (`sumMerge`-style for AggregatingMergeTree), otherwise partial rows of a key show up.

## Checked
2026-11-03. Confirmed against the ClickHouse docs pages "SummingMergeTree" and "AggregatingMergeTree": the engines, `AggregateFunction` columns, `-State` in the materialized view and `-Merge` with GROUP BY at read. Removed: the creation-time and FINAL Verify claims.
Method: documentation only; no commands were run.

---
id: computing-software.database-administration.cockroachdb.cost-based-optimizer-statistics
name: cost-based-optimizer-statistics
category: computing-software
field: database-administration
product: cockroachdb
tags: [cost-based-optimizer, table-statistics, create-statistics, partial-statistics, query-planning]
level: practitioner
status: docs-checked
description: "Tune CockroachDB table statistics for the cost-based optimizer: full, partial and forecasted stats, refresh settings, and per-table storage parameters."
sources:
  - https://www.cockroachlabs.com/docs/stable/cost-based-optimizer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep optimizer statistics fresh enough for good plans without overriding sensible defaults.

The optimizer picks the lowest estimated cost plan; the main factor is cardinality (rows each operator processes). It uses full, partial and forecasted statistics.

Full statistics: generated on table creation and after schema changes, and refreshed when roughly 20% of rows change. A background job covers all indexed columns plus up to 100 non-indexed columns, and multi-column stats on index prefixes. Refresh also follows `IMPORT INTO`, `RESTORE`, and probabilistically after INSERT/UPDATE/DELETE using:
- `sql.stats.automatic_collection.fraction_stale_rows` (default 0.2)
- `sql.stats.automatic_collection.min_stale_rows` (default 500)
Because refresh is probabilistic, stats will not update the instant a threshold is crossed.

Controls:
- Cluster: `sql.stats.automatic_full_collection.enabled`, `sql.stats.automatic_partial_collection.enabled`, plus partial `min_stale_rows` and `fraction_stale_rows`.
- Per table (storage parameters), overriding the cluster: `sql_stats_automatic_full_collection_enabled`, `sql_stats_automatic_collection_fraction_stale_rows`, `sql_stats_automatic_collection_min_stale_rows`, and the `sql_stats_automatic_partial_collection_*` family:
```sql
CREATE TABLE accounts (id INT PRIMARY KEY, balance DECIMAL)
WITH (sql_stats_automatic_collection_enabled = true,
      sql_stats_automatic_collection_min_stale_rows = 1000000);
```

Partial statistics are merged with full ones by default. Manual forms: `CREATE STATISTICS stats ON column FROM table WHERE condition`, or `USING EXTREMES` when `enable_create_stats_using_extremes` is set; columns must be the first key column of a non-inverted index.

Inspect statistics with `SHOW STATISTICS FOR TABLE <table>;`.

## Checked

2026-11-03. Confirmed against the cost-based optimizer page (v26.3 docs source and the published stable page): full and partial statistics settings, storage parameters, refresh settings and defaults, `USING EXTREMES` and its session variable, column selection. Removed: the claim that `created` timestamps and row counts are the verification signal.
Method: documentation only; no commands were run.

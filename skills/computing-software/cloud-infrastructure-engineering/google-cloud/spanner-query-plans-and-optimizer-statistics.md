---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spanner-query-plans-and-optimizer-statistics
name: spanner-query-plans-and-optimizer-statistics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spanner, spanner-query-optimizer, query-plans, spanner-statistics, query-tuning]
level: advanced
status: docs-checked
description: "Tune slow Spanner queries: read execution plans, find hot queries in SPANNER_SYS stats, pin optimizer versions and statistics packages, and use hints like FORCE_INDEX."
sources: ["https://docs.cloud.google.com/spanner/docs/introspection/query-statistics", "https://docs.cloud.google.com/spanner/docs/query-optimizer/overview", "https://docs.cloud.google.com/spanner/docs/query-optimizer/manage-query-optimizer", "https://docs.cloud.google.com/spanner/docs/query-optimizer/versions", "https://docs.cloud.google.com/spanner/docs/sql-best-practices", "https://docs.cloud.google.com/spanner/docs/query-execution-plans"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spanner query plans and optimizer statistics

## 1. Find the queries worth tuning
```sql
SELECT text, execution_count, avg_latency_seconds, avg_cpu_seconds, avg_rows_scanned, avg_rows
FROM SPANNER_SYS.QUERY_STATS_TOP_HOUR
ORDER BY avg_cpu_seconds * execution_count DESC LIMIT 20;
```
`avg_rows_scanned` far above `avg_rows` means a missing or unused index. Also check
`SPANNER_SYS.LOCK_STATS_TOP_*` (contention) and `TXN_STATS_TOP_*`.

## 2. Read the plan
```bash
gcloud spanner databases execute-sql <DB> --instance=<I> --query-mode=PROFILE \
  --sql="SELECT ... " --format=json > plan.json
```
Or the console "Explanation" tab. Look for:
- **Table Scan** over a large table where you expected an **Index Scan**.
- **Distributed Union** fan-out plus a **back join** to the base table (the index lacks a needed column: add `STORING (...)` columns).
- A **Cross Apply** / **Distributed Cross Apply** whose inner side runs per outer row.

## 3. Hints
```sql
SELECT * FROM Orders@{FORCE_INDEX=OrdersByCustomer} WHERE CustomerId = @c;
SELECT ... FROM A JOIN@{JOIN_METHOD=HASH_JOIN} B ON ...;
@{OPTIMIZER_VERSION=9} SELECT ...;
```
Use hints to prove a hypothesis, then fix the schema (index, STORING, interleave) if you can.
Prefer **query parameters** over literals: parameters let Spanner cache and reuse execution plans.

## 4. Optimizer versions and statistics packages
- The optimizer version and stats package can be pinned per database to avoid plan regressions after upgrades:
```sql
ALTER DATABASE db SET OPTIONS (optimizer_version = 9);
ALTER STATISTICS auto_20261010_04_12_33UTC SET OPTIONS (allow_gc = false);
ALTER DATABASE db SET OPTIONS (optimizer_statistics_package = "auto_20261010_04_12_33UTC");
SELECT * FROM INFORMATION_SCHEMA.SPANNER_STATISTICS;
```
- Spanner builds a new statistics package automatically every three days; `ANALYZE` builds one now (it cancels any automatically triggered build, and the new package can take up to ten minutes to be used). Packages are kept 30 days before becoming eligible for garbage collection. As of the 2026-10-24 documentation the latest optimizer version is 9 and the default is 8.
- A package used for a query must have `allow_gc = false` or be pinned; a pinned package is not garbage collected.
- Test a new optimizer version per query with `@{OPTIMIZER_VERSION=...}` before raising the database default; `@{OPTIMIZER_STATISTICS_PACKAGE=...}` does the same for a statistics package.

## Gotchas
- `PROFILE` mode returns rows and statistics (the query runs); `PLAN` returns only the plan.
- `SPANNER_SYS.QUERY_STATS_TOP_MINUTE`, `_10MINUTE` and `_HOUR` hold the queries with the highest CPU in each non-overlapping interval (retention at least 6 hours, 4 days and 30 days respectively).
- A parameterised `LIKE` pattern is not evaluated until execution, so Spanner may read every row; for prefix matches use `STARTS_WITH`. For sparse key lists use `IN UNNEST` with a parameter; `BETWEEN` over sparse keys scans the gaps.

## Verify
- [ ] After the change, `avg_rows_scanned` and `avg_cpu_seconds` for that query fingerprint drop in `QUERY_STATS_TOP_HOUR`.

## Checked
Checked 2026-10-24 against the Spanner query-statistics, query-optimizer overview, manage-query-optimizer, versions, SQL best-practices and execution-plan pages and the gcloud `spanner databases execute-sql` reference (docs.cloud.google.com). Confirmed the `SPANNER_SYS.QUERY_STATS_TOP_*` table and column names, `ALTER DATABASE ... SET OPTIONS` syntax for `optimizer_version` and `optimizer_statistics_package`, the `@{FORCE_INDEX=...}` and `JOIN@{JOIN_METHOD=HASH_JOIN}` hints, the three-day statistics cycle, `ALTER STATISTICS ... allow_gc`, and `--query-mode=PROFILE`. Replaced the optimizer version examples with the current version 9, and removed the Query Insights remark and the unconfirmed index-seek limitations.
Method: documentation only; no commands were run.

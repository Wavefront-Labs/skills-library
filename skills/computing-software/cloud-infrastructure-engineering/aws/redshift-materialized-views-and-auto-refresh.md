---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-materialized-views-and-auto-refresh
name: redshift-materialized-views-and-auto-refresh
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, redshift-materialized-views, auto-refresh, incremental-refresh, query-rewrite]
level: advanced
status: docs-checked
description: "Speed up Redshift queries with materialized views: incremental vs full refresh, AUTO REFRESH, automatic query rewriting, AutoMV and monitoring refresh status."
sources: ["https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-overview.html", "https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html", "https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-refresh-sql-command.html", "https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-auto-mv.html", "https://docs.aws.amazon.com/redshift/latest/dg/r_STV_MV_INFO.html", "https://docs.aws.amazon.com/redshift/latest/dg/r_SVL_MV_REFRESH_STATUS.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redshift materialized views

## 1. Create
```sql
CREATE MATERIALIZED VIEW mv_daily_sales
AUTO REFRESH YES
AS SELECT sale_date, region, SUM(amount) AS revenue, COUNT(*) AS orders
   FROM sales GROUP BY sale_date, region;
```
- `AUTO REFRESH` defaults to `NO`. With `YES` you can add `INTERVAL seconds` (60 to 86,400); without it the
  cluster-wide default applies, 300 seconds unless changed with `ALTER SYSTEM SET default_mv_auto_refresh_interval`.
  Autorefresh runs when cluster resources are available, so freshness is workload-dependent.
- `AUTO REFRESH YES` cannot be used when the definition includes mutable functions or external schemas, or when the
  view is defined on another materialized view.
- Manual: `REFRESH MATERIALIZED VIEW mv_daily_sales;` in the ETL after loads for deterministic freshness. Only the
  owner can refresh, and needs `SELECT` on the base tables.
- Other creation clauses: `BACKUP { YES | NO }` (default YES), `DISTSTYLE`, `DISTKEY`, `SORTKEY`.

## 2. Incremental vs full
Incremental refresh applies only base-table changes. Redshift does not support it for definitions that use outer
joins, set operations (`UNION`, `INTERSECT`, `EXCEPT`, `MINUS`), window functions, subqueries, `DISTINCT`
aggregates, aggregates such as `MEDIAN`, `LISTAGG` and `PERCENTILE_CONT`, mutable functions, or tables from more
than one database. `COUNT`, `SUM`, `MIN`, `MAX` and `AVG` are supported. When incremental refresh is not possible
Redshift performs a full refresh. A manual `VACUUM`, a classic resize, `ALTER DISTKEY`, `ALTER SORTKEY` or a truncate
on a base table forces a full recompute at the next refresh.
```sql
SELECT name, is_stale, state, autorefresh, autorewrite, autorefresh_interval FROM stv_mv_info;
SELECT mv_name, status, starttime, endtime FROM svl_mv_refresh_status ORDER BY starttime DESC LIMIT 20;
```
`state` 1 means incremental, 0 means full recompute on refresh, and 101-105 mean the view cannot be refreshed
because of a dropped or renamed column, changed column type, or renamed table or schema. `is_stale` is `t`, `f` or
`u`. AWS recommends the `SYS_MV_REFRESH_HISTORY` view for new queries over `SVL_MV_REFRESH_STATUS`.

## 3. Automatic query rewriting
Redshift can rewrite queries on base tables to use an up-to-date materialized view. The session setting is
`mv_enable_aqmv_for_session` (`true` or `false`). Rewriting needs the view to be current, so keep it refreshed.

## 4. AutoMV
Redshift creates and drops materialized views itself from workload monitoring, only in low-activity periods, on by
default; turn it off by setting the `auto_mv` parameter-group parameter to `false`. In `EXPLAIN` output, look for
`%_auto_mv_%` to see that one was used. Limits: 200 AutoMVs per database; no new ones at 80% cluster capacity and
they may be dropped at 90%. They cannot contain outer joins, window functions, `DISTINCT`, `HAVING` or other
materialized views, and are not supported on external tables.

## 5. Other uses
Materialized views over Spectrum external tables, streaming ingestion sources and other materialized views; use
`REFRESH MATERIALIZED VIEW ... CASCADE` to refresh a nested set in dependency order (owner or superuser only; it
stops if any view in the cascade cannot refresh).

## Verify
- [ ] Dashboard queries hit the materialized view (`EXPLAIN`) and `is_stale` is `f` after loads.

## Checked
Date: 2026-10-27. Documentation release: Amazon Redshift Database Developer Guide (latest). Confirmed: `AUTO
REFRESH` default, `INTERVAL` range and 300-second cluster default, `AUTO REFRESH YES` restrictions, refresh
permissions, incremental refresh exclusions, forced-recompute operations, `STV_MV_INFO` and
`SVL_MV_REFRESH_STATUS` columns and `state` codes, `mv_enable_aqmv_for_session` name, AutoMV behaviour, limits and
`auto_mv` parameter, and `CASCADE` rules. Removed the claimed default for `mv_enable_aqmv_for_session` (not
readable) and the `mv_tbl__auto_mv` name pattern (the documented pattern is `%_auto_mv_%`).
Method: documentation only; no commands were run.

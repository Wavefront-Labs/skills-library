---
id: computing-software.data-engineering.snowflake.search-optimization-service
name: search-optimization-service
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, search-optimization, point-lookups, equality-predicates, substring-search, variant-search, system-estimate-search-optimization-costs, snowflake-performance, serverless-maintenance]
level: advanced
status: docs-checked
description: "Speed up selective Snowflake lookups with search optimization: when it beats clustering, ON EQUALITY/SUBSTRING per column, estimating cost, and checking the profile."
sources:
  - https://docs.snowflake.com/en/user-guide/search-optimization-service
  - https://docs.snowflake.com/en/sql-reference/functions/system_estimate_search_optimization_costs
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Search optimization service

**Goal:** make needle-in-haystack queries (find one customer's events in billions of rows, filter on an ID that is not the clustering key) return in seconds. Enterprise edition+.

## When it fits
- Highly selective predicates returning a tiny fraction of rows: `where user_id = 42`, `where order_id in (...)`, `where email = '...'`.
- Columns that are **not** the table's clustering key (clustering serves range filters on one leading dimension; search optimization serves many point-lookup columns).
Not for: large scans, aggregations over most of the table, low-cardinality filters.

## Estimate first
```sql
select system$estimate_search_optimization_costs('analytics.events',
  'EQUALITY(user_id, session_id), SUBSTRING(error_message)');
```
Returns a JSON estimate of build, storage and maintenance costs; the page says estimates can differ from actual costs. Maintenance cost is based on recent change activity in the table.

## Enable per column and method
```sql
alter table analytics.events add search optimization on equality(user_id, session_id);
alter table analytics.events add search optimization on substring(error_message);
alter table analytics.events add search optimization on equality(payload:device.id);   -- VARIANT path
describe search optimization on analytics.events;      -- shows active expressions and build status
alter table analytics.events drop search optimization on substring(error_message);
```
Avoid table-wide `add search optimization;` (all eligible columns: expensive).

## Verify it's used
Query profile shows search optimization being used and partitions scanned far below total. Build takes time after enabling: check the `search_optimization_progress` column of `SHOW TABLES` before measuring.

## Cost tracking
Monitor search optimization costs and revisit tables whose lookups disappeared.

## Verify
- [ ] Before/after query profile: partitions scanned and elapsed time drop for the target lookup.
- [ ] Monthly credits match the estimate within a reasonable margin.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the search optimization enabling page, the service overview and the cost-estimate function page: Enterprise Edition requirement, ALTER TABLE ... ADD SEARCH OPTIMIZATION ON EQUALITY(...) / SUBSTRING(...) / GEO, VARIANT path form such as EQUALITY(c4:user.uuid), DROP SEARCH OPTIMIZATION ON, DESCRIBE SEARCH OPTIMIZATION, SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS, search_optimization_progress in SHOW TABLES.

Removed earlier: substring/geospatial history claims and account_usage views.

Method: documentation only; no commands were run.

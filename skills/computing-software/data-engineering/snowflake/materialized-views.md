---
id: computing-software.data-engineering.snowflake.materialized-views
name: materialized-views
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-materialized-views, materialized-view, query-rewrite, mv-maintenance, aggregation-acceleration, clustering-mv, snowflake-performance]
level: advanced
status: docs-checked
description: "Use Snowflake materialized views for repeated single-table aggregations: restrictions, background maintenance cost, query rewrite, clustering an MV, vs dynamic tables."
sources:
  - https://docs.snowflake.com/en/user-guide/views-materialized
  - https://docs.snowflake.com/en/sql-reference/sql/create-materialized-view
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake materialized views

**Goal:** precompute an expensive projection/aggregation over one large table so frequent queries read the small result, always consistent with the base table. Enterprise edition+.

## Fit
- Single base table (no joins), frequently queried with the same aggregation or filter.
- Base table changes slowly relative to query frequency (maintenance cost scales with changes).
- Alternate clustering: an MV with a different clustering key than the base table serves a second access pattern.

```sql
create materialized view analytics.mv_daily_sales
  cluster by (sale_date)
as
select sale_date, store_id, sum(amount) as amount, count(*) as txns
from analytics.sales
group by sale_date, store_id;
```

## Restrictions (main ones)
- A single table; no joins (including self-joins), no window functions, no `having`, no `order by`, no `limit`; every GROUP BY key must be in the SELECT list; only a documented list of aggregate functions (for example SUM, COUNT, MIN, MAX, AVG, APPROX_COUNT_DISTINCT). See the limitations section of the page.
For anything more complex, use dynamic tables or scheduled tables.

## Maintenance and freshness
- A background process automatically maintains the view; timing depends on the workload on the base table and the view.
- Maintenance cost can be monitored with the `MATERIALIZED_VIEW_REFRESH_HISTORY` table function (Information Schema). High-churn base tables make MVs more expensive to maintain.
- Suspend and resume are available through ALTER MATERIALIZED VIEW.

## Query rewrite
Queries on the base table can be rewritten to use the MV; check the query profile for the MV being scanned.

## MV vs dynamic table vs table
| Need | Choose |
|---|---|
| Single-table aggregation maintained automatically, query rewrite | Materialized view |
| Joins/complex SQL with tolerable lag | Dynamic table |
| Full control of schedule/logic | Table built by dbt/tasks |

## Verify
- [ ] Target dashboard query time drops and its profile scans the MV.
- [ ] Monthly MV refresh credits are less than the compute saved.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: Enterprise Edition requirement, single table and no joins/window functions/HAVING/ORDER BY/LIMIT, GROUP BY keys must be in SELECT, CLUSTER BY requires a column list, background maintenance, MATERIALIZED_VIEW_REFRESH_HISTORY table function (views-materialized and create-materialized-view pages).

Removed or corrected: the 'no UDFs' and 'non-deterministic' restrictions as worded, the always-current claim, and the account_usage view path (not on the pages read).

Method: documentation only; no commands were run.

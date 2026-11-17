---
id: computing-software.data-engineering.snowflake.serverless-feature-costs
name: serverless-feature-costs
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, cost-control, serverless-credits, metering-history, automatic-clustering, snowpipe, search-optimization, cloud-services]
level: practitioner
status: docs-checked
description: "Find serverless Snowflake spend (Snowpipe, auto-clustering, search optimization, MVs, serverless tasks, replication) via METERING_HISTORY and per-feature views."
sources:
  - https://docs.snowflake.com/en/user-guide/cost-exploring-compute
  - https://docs.snowflake.com/en/sql-reference/account-usage/metering_history
  - https://docs.snowflake.com/en/user-guide/cost-understanding-compute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serverless feature costs

**Goal:** credits that do not show up on any warehouse are found and attributed to objects.

## Where serverless credits come from
Serverless features use compute that Snowflake manages instead of a virtual warehouse. They are billed on compute-hours measured per second, with a per-feature credits-per-compute-hour rate listed in the "Serverless Feature Credit Table" of the Snowflake Service Consumption Table (read it for current rates). Each serverless feature appears as its own bill line item, with Snowflake-managed compute and cloud services shown together. Examples with their own account-usage views: Snowpipe, automatic clustering, search optimization, materialized view refresh, serverless tasks, replication, query acceleration. Hybrid table requests are no longer billed (metering stopped in 2026, so that view records no new events).

Cloud services are billed only when daily cloud services usage exceeds 10% of daily warehouse usage (computed daily in UTC). Serverless compute does not count toward that 10% adjustment.

## Account-level breakdown
```sql
select service_type, sum(credits_used) credits
from snowflake.account_usage.metering_history
where start_time >= dateadd(day, -30, current_timestamp())
group by 1 order by 2 desc;
```
`METERING_HISTORY` separates warehouse consumption (`WAREHOUSE_METERING`) from each serverless feature (for example `PIPE` for Snowpipe); cloud services compute is included in warehouse consumption there. `CREDITS_USED` does not include the cloud services adjustment, so it can exceed what you are billed. The view can lag up to 180 minutes (6 hours for the cloud services column). Run `select distinct service_type` to see the values in your account.

## Per-object views
```sql
-- clustering by table
select database_name, schema_name, table_name, sum(credits_used) c
from snowflake.account_usage.automatic_clustering_history
where start_time >= dateadd(day, -30, current_timestamp()) group by 1,2,3 order by c desc limit 20;

-- search optimization by table
select table_name, sum(credits_used) from snowflake.account_usage.search_optimization_history
where start_time >= dateadd(day,-30,current_timestamp()) group by 1 order by 2 desc;

-- Snowpipe by pipe
select pipe_name, sum(credits_used) credits
from snowflake.account_usage.pipe_usage_history
where start_time >= dateadd(day,-30,current_timestamp()) group by 1 order by 2 desc;

-- serverless tasks
select task_name, sum(credits_used) from snowflake.account_usage.serverless_task_history
where start_time >= dateadd(day,-30,current_timestamp()) group by 1 order by 2 desc;

-- MV refresh
select table_name, sum(credits_used) from snowflake.account_usage.materialized_view_refresh_history
where start_time >= dateadd(day,-30,current_timestamp()) group by 1 order by 2 desc;
```
Related views: `QUERY_ACCELERATION_HISTORY`, `REPLICATION_GROUP_USAGE_HISTORY` (replication or failover groups), `DATABASE_REPLICATION_USAGE_HISTORY`.

## Acting on what you find
- **Snowpipe:** the cost page shows a query of average file size per table by ingest method (COPY or Snowpipe); file sizes that are too small or too large for optimal ingest need investigation.
- **Auto-clustering, search optimization, MV refresh, serverless tasks:** rank objects by credits with the queries above and ask whether each object still earns its cost; drop or suspend what does not (check the relevant command reference before running it).
- **Cloud services above 10%:** find the queries and warehouses with the highest cloud services usage using the sample queries on the Exploring compute cost page.

## Verify
- [ ] Monthly report of serverless credits by service type and top objects.
- [ ] Per-object totals roughly reconcile with `METERING_HISTORY` for the same period.

## Checked
2026-11-09. Confirmed against "Exploring compute cost", "Understanding compute cost" and the METERING_HISTORY view page: serverless billing model, 10% cloud services rule and exclusion of serverless, service type WAREHOUSE_METERING and PIPE, view names and lists, hybrid table billing note, view latency, CREDITS_USED caveat. Removed: the full SERVICE_TYPE value list, the 0.06 credits per 1000 files figure and the 100-250 MB batching advice, specific suspend/drop SQL and the system functions, the Budgets and resource monitor claims, and the dynamic table remark, because the fetched pages did not confirm them.
Method: documentation only; no commands were run.

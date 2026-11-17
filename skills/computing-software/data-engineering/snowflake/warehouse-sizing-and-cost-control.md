---
id: computing-software.data-engineering.snowflake.warehouse-sizing-and-cost-control
name: warehouse-sizing-and-cost-control
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, virtual-warehouse, warehouse-sizing, credits, cost-control, finops, auto-suspend, auto-resume, multi-cluster-warehouse, scaling-policy, resource-monitor, query-profile, spilling, account-usage, warehouse-metering-history, query-history, statement-timeout]
level: practitioner
status: docs-checked
description: "Right-size Snowflake warehouses and cap spend: credits per size, AUTO_SUSPEND, multi-cluster scaling, resource monitors, spill in Query Profile, ACCOUNT_USAGE costs."
sources:
  - https://docs.snowflake.com/en/user-guide/warehouses-overview
  - https://docs.snowflake.com/en/user-guide/cost-understanding-compute
  - https://docs.snowflake.com/en/user-guide/resource-monitors
  - https://docs.snowflake.com/en/sql-reference/account-usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake warehouse sizing and cost control — pay for work, not idle

**Goal:** give each workload a warehouse that finishes on time at the lowest credit burn, and put hard guardrails on runaway spend.

## 1. The billing model
- Gen1 standard warehouse credits per hour: X-Small 1, Small 2, Medium 4, Large 8, X-Large 16, 2X-Large 32, 3X-Large 64, 4X-Large 128, 5X-Large 256 (doubling each step). Gen2 and Snowpark-optimized warehouses differ; check the current pricing table.
- Minimum charge on each start is 60 seconds, then per second. A warehouse that runs 30 to 60 seconds is billed for 60; one that runs 61 seconds, stops, and restarts for under 60 seconds is billed for 121 seconds.
- Cloud services are charged only if daily consumption exceeds 10% of daily virtual warehouse usage (calculated daily, UTC). Serverless compute is not part of that adjustment.
- Larger is not necessarily faster for small, basic queries.

## 2. Separate and size warehouses by workload
Create one warehouse per workload class (`LOAD_WH`, `TRANSFORM_WH`, `BI_WH`, `ADHOC_WH`) so you can size, suspend and attribute each one.
```sql
CREATE WAREHOUSE TRANSFORM_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60          -- seconds
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  STATEMENT_TIMEOUT_IN_SECONDS = 3600;
```
Sizing method: run a representative workload at two or three sizes and pick the smallest size that meets the SLA with little or no spilling in Query Profile.
- Each running warehouse keeps a cache of table data; the cache is dropped when the warehouse suspends (and when it is sized down). Trade credits saved by suspending against re-reading data afterwards.
- Set `AUTO_SUSPEND` to match the gaps in your workload: with regular gaps of 2 or 3 minutes between queries, a 1 or 2 minute value only causes repeated resume charges.
- Set `STATEMENT_TIMEOUT_IN_SECONDS` per warehouse so runaway queries stop.

## 3. Concurrency: scale out for queuing
Multi-cluster warehouses need Enterprise Edition or higher. Snowflake recommends them for automated scaling when queries queue.
```sql
ALTER WAREHOUSE BI_WH SET MIN_CLUSTER_COUNT = 1 MAX_CLUSTER_COUNT = 4 SCALING_POLICY = 'STANDARD';
```
`STANDARD` (default) starts extra clusters to prevent queuing; `ECONOMY` keeps running clusters fully loaded and only starts another if it estimates enough load to keep it busy for at least 6 minutes, so queries may queue. Check `QUEUED_OVERLOAD_TIME` (milliseconds in the warehouse queue because of overload) in `ACCOUNT_USAGE.QUERY_HISTORY`.

## 4. Read Query Profile for spill
In Snowsight, Query Profile statistics show Bytes spilled to local storage and Bytes spilled to remote storage. Spilling happens when an operation's intermediate results do not fit in memory and can have a profound effect on performance, especially when remote disk is used. Options are a larger warehouse or reducing the data the operator holds (see exploding-joins-and-query-anti-patterns). Also compare Partitions scanned with Partitions total to judge pruning.

## 5. Guardrails: resource monitors
```sql
CREATE RESOURCE MONITOR ADHOC_MONTHLY WITH CREDIT_QUOTA = 500
  FREQUENCY = MONTHLY START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 75 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND
           ON 110 PERCENT DO SUSPEND_IMMEDIATE;
ALTER WAREHOUSE ADHOC_WH SET RESOURCE_MONITOR = ADHOC_MONTHLY;
```
- `SUSPEND` suspends after running statements complete; `SUSPEND_IMMEDIATE` cancels running statements.
- Resource monitors work for warehouses only, not serverless features (Snowpipe, automatic reclustering, materialized views) or AI services; use a budget for those.
- Monitor limits count all cloud services consumption, with no 10% adjustment.

## 6. Find where credits go
```sql
SELECT warehouse_name, SUM(credits_used) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY 1 ORDER BY 2 DESC;
```
- ACCOUNT_USAGE views have latency: QUERY_HISTORY up to 45 minutes, WAREHOUSE_METERING_HISTORY up to 3 hours (maximums). Historical views keep 1 year. INFORMATION_SCHEMA has no latency but shorter retention.

## Verify
- [ ] Every warehouse has `AUTO_SUSPEND` set to match its query gaps and `AUTO_RESUME = TRUE`.
- [ ] Each production warehouse is attached to a resource monitor with a suspend trigger.
- [ ] Top costly queries from the last 30 days were checked for remote spill and poor pruning.
- [ ] Size changes were justified by a before/after runtime and credit comparison.

## Checked
2026-11-09. Confirmed against the Snowflake docs "Overview of warehouses", "Warehouse considerations", "Multi-cluster warehouses", "Working with resource monitors", "Understanding compute cost", the Account Usage overview and the QUERY_HISTORY and WAREHOUSE_METERING_HISTORY pages: credit table, 60 second minimum, cache drop on suspend, scaling policies including the 6 minute rule, SUSPEND vs SUSPEND_IMMEDIATE, serverless exclusion, 10% cloud services rule, latency and retention. Removed as unconfirmed: the "2x faster per size" rule, the 172800 second timeout default, 300 to 600 second BI auto-suspend advice, query tagging, and the automatic clustering section.
Method: documentation only; no commands were run.

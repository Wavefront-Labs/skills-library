---
id: computing-software.data-engineering.data-warehouse-architecture.serving-slas-and-query-concurrency
name: serving-slas-and-query-concurrency
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, serving-concurrency, serving-sla, multi-cluster-warehouse, query-queuing, workload-management, result-cache]
level: practitioner
status: docs-checked
description: "Meet serving SLAs under concurrency: defining latency SLOs, warehouse queuing and multi-cluster scaling, workload management, caching layers, pre-aggregation and load testing."
sources:
  - https://docs.snowflake.com/en/user-guide/warehouses-multicluster
  - https://docs.aws.amazon.com/redshift/latest/dg/cm-c-implementing-workload-management.html
  - https://cloud.google.com/bigquery/docs/slots
  - https://docs.databricks.com/en/compute/sql-warehouse/warehouse-behavior.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serving SLAs and concurrency

## Define the SLA in measurable terms
- Latency SLO per query class, set from your own users' needs (for example one target for dashboard tiles, another for API lookups, another for ad hoc).
- Concurrency target: peak simultaneous users/queries (Monday 9 am, month-end).
- Freshness SLO separately (data age), since caching trades freshness for latency.
Measure from query history (queued time vs execution time) and from the client side.

## Why warehouses miss concurrency SLAs
A compute cluster has finite resources, so extra queries **queue**: Snowflake queues additional queries when resources are insufficient, BigQuery queues units of work when a query asks for more slots than are available (slot contention lengthens job runtime), and Databricks places a query in a queue when there is no capacity. Queue time, not execution time, is often what breaks p95 at peak, so report it separately in query history.

## Levers
| Lever | Platform examples |
|---|---|
| Scale out for concurrency | Snowflake multi-cluster warehouses (`MIN_CLUSTER_COUNT` / `MAX_CLUSTER_COUNT`; in Auto-scale mode Snowflake starts extra clusters when queries queue, and `SCALING_POLICY` of `STANDARD` or `ECONOMY` trades responsiveness against credits), Databricks SQL warehouse min/max clusters, Redshift concurrency scaling, BigQuery reservation autoscaling |
| Scale up for heavy queries | larger cluster size; on Databricks, increase size if the query profile shows spill to disk |
| Workload isolation | separate warehouses/reservations for BI vs ELT vs data science; Redshift automatic WLM queues with query priorities (High/Normal/Low), or manual WLM queues routed by user group or query group, with query monitoring rules (QMR) to limit long-running queries |
| Caching | BI tool caches and API caches with a TTL matched to the freshness SLO; check each warehouse's own result-cache rules |
| Pre-aggregation | aggregate tables/materialised views for dashboard grain; BI extracts |
| Specialised serving store | a separate low-latency store for high-QPS APIs when the warehouse cannot meet the target |
| Query hygiene | limit result sizes, avoid SELECT *, use partition/cluster pruning |

Platform notes:
- Snowflake: the maximum credits per hour for a multi-cluster warehouse is the per-cluster rate for its size multiplied by MAX_CLUSTER_COUNT, so bound the maximum.
- Databricks: serverless SQL warehouses autoscale clusters when queue wait times rise; Databricks recommends serverless for most workloads. For classic and pro warehouses it recommends one cluster per 10 concurrent queries, a queued query waiting 5 minutes triggers scale-up, and the maximum queue length is 1,000 queries. Watch the Peak Queued Queries metric: consistently above 0 means a larger size or more clusters.
- Redshift: for manual WLM AWS recommends 15 or fewer query slots in total, and in most cases recommends automatic WLM. Switching WLM mode needs a cluster reboot.
- BigQuery: unassigned projects can fall back to on-demand pricing, so assign reservations at folder or organization level.

## Load test before launch
- Replay realistic query mixes (from query history or BI tool logs) at target concurrency against the SQL endpoint or dashboard.
- Run once with the result cache disabled to measure worst case (the setting is platform-specific), then again with it to see realistic behaviour.
- Watch queue time, spill to disk, and scaling events.

## Operating
- Alert on SLO burn (latency, queue time) per workload, not just on failures.
- Review regularly: top queries by total time at peak, cache hit rates, scaling costs.

## Verify
- [ ] Load test at peak concurrency meets latency targets with cache disabled.
- [ ] Queue time at peak hours stays below threshold; scaling bounded by max clusters/budget.

## Checked
Date: 2026-11-09. Confirmed from the four cited pages: Snowflake multi-cluster behaviour, scaling policy names and credit ceiling; Redshift automatic vs manual WLM, priorities, QMR, 15-slot advice and reboot on mode switch; BigQuery slot queuing and contention, folder-level reservation assignment; Databricks serverless autoscaling, sizing advice, queue limit and classic/pro scaling rules. Removed as unconfirmed: the Snowflake query_history SQL, example latency numbers, USE_CACHED_RESULT, JMeter/k6, named serving stores, and the Redshift per-minute concurrency scaling cost. The result-cache and caching rows are general advice, not page-confirmed.
Method: documentation only; no commands were run.

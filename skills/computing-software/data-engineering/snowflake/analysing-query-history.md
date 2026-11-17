---
id: computing-software.data-engineering.snowflake.analysing-query-history
name: analysing-query-history
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-query-history, query-history, spilling, queued-overload, partitions-scanned, query-hash, snowflake-performance]
level: practitioner
status: docs-checked
description: "Mine Snowflake ACCOUNT_USAGE.QUERY_HISTORY for slow and expensive queries: spilling, queueing, poor pruning, repeated query_hash patterns, and per-user/warehouse rollups."
sources:
  - https://docs.snowflake.com/en/sql-reference/account-usage/query_history
  - https://docs.snowflake.com/en/user-guide/performance-query-exploring
  - https://docs.snowflake.com/en/sql-reference/account-usage/query_attribution_history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysing QUERY_HISTORY

**Goal:** find the handful of query patterns that drive most runtime and cost, and the specific symptom for each.

`snowflake.account_usage.query_history` keeps 365 days (latency up to ~45 min). `information_schema.query_history()` table function: the past 7 days only.

## Top patterns by total time (group by parameterized hash)
```sql
select query_parameterized_hash,
       any_value(query_text) sample_text,
       count(*) runs,
       sum(total_elapsed_time)/1000/3600 total_hours,
       avg(total_elapsed_time)/1000 avg_s,
       any_value(warehouse_name) wh
from snowflake.account_usage.query_history
where start_time > dateadd(day, -7, current_timestamp())
  and execution_status = 'SUCCESS'
group by 1 order by total_hours desc limit 25;
```
`query_parameterized_hash` groups queries differing only in literals (dashboards with filter values).

## Symptom columns
```sql
select query_id, warehouse_name, warehouse_size, total_elapsed_time/1000 s,
       queued_overload_time/1000 queued_s,
       bytes_spilled_to_local_storage/power(1024,3) spill_local_gb,
       bytes_spilled_to_remote_storage/power(1024,3) spill_remote_gb,
       partitions_scanned, partitions_total,
       round(partitions_scanned / nullif(partitions_total,0), 3) scan_ratio,
       rows_produced, compilation_time/1000 compile_s
from snowflake.account_usage.query_history
where start_time > dateadd(day, -1, current_timestamp()) and total_elapsed_time > 60000
order by total_elapsed_time desc limit 50;
```
| Symptom | Meaning | Action |
|---|---|---|
| `queued_overload_time` high | warehouse saturated | multi-cluster, separate workloads, reschedule |
| remote spilling > 0 | memory exhausted | bigger warehouse, reduce data earlier, fix exploding joins |
| `scan_ratio` near 1 on big tables with selective filters | no pruning | clustering key, filter on clustered column, avoid functions on filter column |
| high `compilation_time` | huge SQL / many views / complex metadata | simplify, avoid massive IN lists |
| `rows_produced` huge for BI | missing aggregation, exports | push aggregation to SQL, limit |

## Cost per query
```sql
select query_id, warehouse_name, credits_attributed_compute, credits_used_query_acceleration
from snowflake.account_usage.query_attribution_history
where start_time > dateadd(day,-7,current_timestamp()) order by 3 desc limit 20;
```
Roll up by `user_name`, `role_name` or `query_tag` for chargeback.

## Next step on a culprit
Open the Query Profile (Snowsight, or `get_query_operator_stats(query_id)`) to find the expensive operator:
```sql
select * from table(get_query_operator_stats('01b3...'));
```

## Gotchas
- QUERY_HISTORY has separate `execution_time` and `compilation_time` columns besides `total_elapsed_time`; compare them before blaming compute.

## Verify
- [ ] Weekly top-25 report by parameterized hash reviewed; owners assigned.
- [ ] After a fix, the same hash shows lower avg time/credits.

## Checked
2026-10-28. Confirmed against the QUERY_HISTORY and QUERY_ATTRIBUTION_HISTORY view pages and the performance exploration page (365 days, latency up to 45 minutes, 7 days for the information_schema function, query_parameterized_hash, queued_overload_time, bytes_spilled_to_local_storage and bytes_spilled_to_remote_storage, partitions_scanned, partitions_total, compilation_time, execution_time, warehouse_size, credits_used_query_acceleration, GET_QUERY_OPERATOR_STATS). Removed: RESULT_REUSE and redaction remarks.
Method: documentation only; no commands were run.

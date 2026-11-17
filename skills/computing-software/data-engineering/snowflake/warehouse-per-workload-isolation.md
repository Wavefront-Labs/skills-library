---
id: computing-software.data-engineering.snowflake.warehouse-per-workload-isolation
name: warehouse-per-workload-isolation
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, virtual-warehouse, workload-isolation, warehouse-design, cost-control, concurrency, rbac, chargeback]
level: practitioner
status: docs-checked
description: "Design a Snowflake warehouse layout per workload (ingest, transform, BI, ad hoc, data science): sizing, grants, defaults per user/service, and avoiding noisy neighbours."
sources:
  - https://docs.snowflake.com/en/user-guide/warehouses-considerations
  - https://docs.snowflake.com/en/user-guide/warehouses-multicluster
  - https://docs.snowflake.com/en/sql-reference/sql/alter-user
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warehouse-per-workload isolation

**Goal:** a heavy dbt run never slows dashboards, costs are attributable per workload, and each warehouse is sized for its own query shape.

## Typical layout
| Warehouse | Users | Shape | Starting config |
|---|---|---|---|
| `LOAD_WH` | Fivetran/Airbyte/COPY services | many small writes | XS-S, auto_suspend 60 |
| `TRANSFORM_WH` | dbt/Airflow service users | big scans, joins, few concurrent | M-L, auto_suspend 60, single cluster |
| `TRANSFORM_XL_WH` | specific heavy models (`snowflake_warehouse` config) | very large | XL, used briefly |
| `BI_WH` | BI tool service account | many small concurrent queries | S, multi-cluster 1-4, scaling policy STANDARD |
| `ADHOC_WH` | analysts | unpredictable | S-M, statement timeout 30 min, resource monitor |
| `DS_WH` | data science | memory-heavy Python | M |

```sql
create warehouse if not exists BI_WH
  warehouse_size = 'SMALL'
  min_cluster_count = 1 max_cluster_count = 4 scaling_policy = 'STANDARD'
  auto_suspend = 60 auto_resume = true initially_suspended = true
  statement_timeout_in_seconds = 600
  comment = 'Dashboards via Tableau service user';
```

## Access and defaults
```sql
grant usage on warehouse BI_WH to role BI_READER;
alter user SVC_TABLEAU set default_warehouse = BI_WH default_role = BI_READER;
alter user SVC_DBT set default_warehouse = TRANSFORM_WH;
```
Grant warehouses to functional roles, not to users. Revoke `USAGE` on big warehouses from ad hoc roles to stop "just use the XL".

## Why isolate
- Concurrency queuing is per warehouse: BI queries queue behind long transforms on a shared one.
- Cache: the warehouse local disk cache is per warehouse; BI benefits from a warm, dedicated warehouse; transforms evict it.
- Attribution: usage and load views report per warehouse, which makes chargeback straightforward.
- Different tuning: multi-cluster for concurrency (BI) vs larger size for single big queries (transform).

## Anti-patterns
- One warehouse per person/team with low utilisation: many mostly idle warehouses and cold caches. Isolate by workload shape, not org chart; use query tags for team attribution.
- Multi-cluster on transform warehouses to "speed up" a single long query: multi-cluster adds concurrency, not single-query speed.

## Monitoring per warehouse
```sql
select warehouse_name, avg(avg_queued_load) q, avg(avg_running) r
from snowflake.account_usage.warehouse_load_history
where start_time >= dateadd(day, -7, current_timestamp()) group by 1;
```
Persistent `avg_queued_load > 0` on BI -> raise max clusters; on transform -> size up or spread schedule.

## Verify
- [ ] Each service user has the intended default warehouse; ad hoc roles cannot use transform warehouses.
- [ ] Resource monitors attached to ADHOC and DS warehouses.

## Checked
2026-10-28. Confirmed against the Snowflake multi-cluster warehouse page (MIN_CLUSTER_COUNT, SCALING_POLICY), CREATE WAREHOUSE parameters (STATEMENT_TIMEOUT_IN_SECONDS), the performance exploration page (WAREHOUSE_LOAD_HISTORY with avg_running and avg_queued_load) and the QUERY_HISTORY view (local disk cache). Removed: the WAREHOUSE_METERING_HISTORY query and claim, Snowpark-optimized warehouse row and the 60-second minimum billing remark. The table of starting configurations is sizing guidance, not a documented limit.
Method: documentation only; no commands were run.

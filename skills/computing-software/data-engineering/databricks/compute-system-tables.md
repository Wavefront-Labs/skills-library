---
id: computing-software.data-engineering.databricks.compute-system-tables
name: compute-system-tables
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, compute-system-tables, system-compute, utilization, cost-optimization]
level: practitioner
status: docs-checked
description: "Use system.compute tables to audit clusters and SQL warehouses: configuration history, node utilization timelines, warehouse events, and finding idle or oversized compute."
sources:
  - https://docs.databricks.com/aws/en/admin/system-tables/compute
  - https://docs.databricks.com/aws/en/admin/system-tables/warehouse-events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# system.compute cluster and warehouse tables

**Goal:** find idle, oversized or misconfigured compute with SQL.

## Tables
- `system.compute.clusters`: SCD history of cluster configs (`change_time`, `cluster_name`, `owned_by`, `driver_node_type`, `worker_node_type`, `auto_termination_minutes`, `dbr_version`, tags).
- `system.compute.node_types`: hardware per node type.
- `system.compute.node_timeline`: per-node, per-minute utilisation (`cpu_user_percent`, `cpu_system_percent`, `mem_used_percent`, network).
- `system.compute.warehouse_events` (`event_type`: STARTING, RUNNING, SCALED_UP, SCALED_DOWN, STOPPING, STOPPED), one row each time a SQL warehouse starts, stops, runs or scales.
- Also `system.compute.instance_events` and `system.compute.instance_pools` (both Public Preview).

## Queries
```sql
-- latest config per cluster with no auto termination
WITH latest AS (
  SELECT *, row_number() OVER (PARTITION BY cluster_id ORDER BY change_time DESC) rn
  FROM system.compute.clusters)
SELECT cluster_id, cluster_name, owned_by FROM latest
WHERE rn = 1 AND delete_time IS NULL AND (auto_termination_minutes IS NULL OR auto_termination_minutes = 0);

-- under-utilised clusters (low average CPU over the last 7 days; pick your own threshold)
SELECT cluster_id, avg(cpu_user_percent + cpu_system_percent) avg_cpu, avg(mem_used_percent) avg_mem
FROM system.compute.node_timeline
WHERE start_time >= current_date() - 7
GROUP BY cluster_id HAVING avg_cpu < 20 ORDER BY avg_cpu;

-- warehouse scaling events per day
SELECT warehouse_id, date(event_time) d, count_if(event_type = 'SCALED_UP') ups
FROM system.compute.warehouse_events GROUP BY ALL ORDER BY d DESC;
```
Join with `system.billing.usage` on `usage_metadata.cluster_id` to put usage next to cluster configuration; billing records are cross-regional but cluster records are region-specific, so run the query in the matching region.

## Gotchas
- The classic compute tables (clusters, node_timeline) cover all-purpose and jobs compute and do not contain serverless compute or SQL warehouses.
- Nodes that ran under 10 minutes might not appear in node_timeline; records are typically available within one hour.
- `clusters` keeps every config change; always take the latest row per cluster.

## Verify
Pick one flagged cluster and confirm in the compute UI metrics that utilisation is low.

## Checked
2026-11-01: confirmed against the Databricks compute system tables and warehouse events reference pages: table names, column names (auto_termination_minutes, cpu_user_percent, cpu_system_percent, mem_used_percent, delete_time, change_time), warehouse event types, serverless and short-node limitations. Removed: system.compute.warehouses (not listed), the 20% threshold, the warehouse_id billing join.
Method: documentation only; no commands were run.

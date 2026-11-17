---
id: computing-software.cloud-infrastructure-engineering.azure.flexible-server-monitoring-query-store-and-slow-query-logs
name: flexible-server-monitoring-query-store-and-slow-query-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, open-source-databases, flexible-server-monitoring, slow-query-log, query-store-postgres, query-performance-insight]
level: advanced
status: docs-checked
description: "Monitor Azure Database for PostgreSQL and MySQL flexible servers: key metrics, Query Store and pg_stat_statements, slow query logs to Log Analytics, and alerts."
sources: ["https://learn.microsoft.com/azure/postgresql/flexible-server/concepts-query-store", "https://learn.microsoft.com/azure/mysql/flexible-server/concepts-slow-query-logs", "https://learn.microsoft.com/azure/postgresql/flexible-server/concepts-monitoring", "https://learn.microsoft.com/azure/postgresql/flexible-server/concepts-query-performance-insight"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flexible server monitoring

**Goal:** find the slow queries and resource limits behind database complaints on PostgreSQL/MySQL flexible servers.

## Metrics to alert on
CPU percent, memory percent, storage percent, IOPS consumed vs provisioned, active connections vs `max_connections`, replication lag, transaction ID age (PostgreSQL). Some PostgreSQL metrics are only emitted when `metrics.collector_database_activity` is `ON` (dynamic, no restart). Pick alert thresholds from the metrics page; check metric names there.

## PostgreSQL
- **Query Store**: `pg_qs.query_capture_mode` = `top` or `all` (dynamic), `pgms_wait_sampling.query_capture_mode = all` for wait sampling. Data lives in the `azure_sys` database.
- **Query Performance Insight** depends on Query Store data (and wait sampling data for wait views).
- Slow-statement logging for PostgreSQL: look up the server parameters and diagnostic-settings log categories on the PostgreSQL logging pages (not verified here).

## MySQL
```bash
az mysql flexible-server parameter set -g rg -s mysql1 -n slow_query_log --value ON
az mysql flexible-server parameter set -g rg -s mysql1 -n long_query_time --value 2   # default is 10 s
```
Send the slow query log to Log Analytics through a diagnostic setting; see the slow query logs page for the category and table names.

## Gotchas
- Logging every statement fills storage and costs ingestion; keep thresholds sane.

## Verify
- [ ] A deliberately slow query (`SELECT pg_sleep(2)` / `SELECT SLEEP(3)`) appears in the logs table within minutes.

## Checked
2026-10-28. Confirmed on the PostgreSQL monitoring and Query Store pages and MySQL slow query log page: `metrics.collector_database_activity`, `pg_qs.query_capture_mode` (ALL or TOP, dynamic), `pgms_wait_sampling.query_capture_mode`, `azure_sys` database, MySQL `slow_query_log` (off by default) and `long_query_time` (default 10 s). Removed as unconfirmed: view names, pg_stat_statements steps, PostgreSQL log parameter and category, MySqlSlowLogs query, log_slow_admin_statements, log_queries_not_using_indexes, credits and overhead advice, the 80% threshold.
Method: documentation only; no commands were run.

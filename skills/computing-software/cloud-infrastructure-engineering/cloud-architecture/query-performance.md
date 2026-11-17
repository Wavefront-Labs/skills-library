---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.query-performance
name: query-performance
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, query-performance, explain-analyze, slow-query-log, performance-insights, query-store, index-tuning]
level: practitioner
status: draft
description: "Review query performance in managed databases: find top queries by load, read EXPLAIN plans, fix indexes and N+1s, and verify gains with Performance Insights or Query Store."
sources: ["https://www.postgresql.org/docs/current/using-explain.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html", "https://learn.microsoft.com/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database query performance review

## Find the queries
- PostgreSQL: `pg_stat_statements` (order by `total_exec_time`), `auto_explain`, `log_min_duration_statement`.
- MySQL: slow query log, Performance Schema digests.
- SQL Server / Azure SQL: Query Store (top resource consumers, regressed queries).
- Managed: RDS Performance Insights / CloudWatch Database Insights (DB load by wait event and SQL),
  Cloud SQL Query Insights, Azure Query Performance Insight.

Prioritise by **total load** (calls x time), not just slowest single execution.

## Diagnose
`EXPLAIN (ANALYZE, BUFFERS)` in PostgreSQL:
- Seq Scan on large tables with selective filters -> missing index.
- Rows estimated vs actual off by orders of magnitude -> stale statistics (`ANALYZE`), correlated columns (extended statistics).
- Nested Loop over many rows -> join strategy/index issue.
- Sort/Hash spilling to disk -> `work_mem` or query reshaping.

## Fix ladder
1. Index (composite in filter/sort order; covering/INCLUDE; partial indexes).
2. Rewrite (avoid functions on indexed columns, SELECT only needed columns, keyset pagination
   instead of OFFSET).
3. Remove N+1 in the ORM (eager loading / batching).
4. Caching or materialized views for heavy aggregates.
5. Only then scale hardware.

## Gotchas
- Adding indexes slows writes and costs storage; drop unused ones (`pg_stat_user_indexes.idx_scan = 0`).
- Testing on tiny dev data gives different plans.

## Verify
- [ ] Before/after DB load and query latency recorded.

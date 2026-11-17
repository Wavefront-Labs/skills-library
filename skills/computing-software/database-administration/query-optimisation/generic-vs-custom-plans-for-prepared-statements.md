---
id: computing-software.database-administration.query-optimisation.generic-vs-custom-plans-for-prepared-statements
name: generic-vs-custom-plans-for-prepared-statements
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, execution-plan, generic-plan, plan-cache-mode, prepared-statements, parameter-sniffing, bind-variables]
level: advanced
status: draft
description: "Understand when databases reuse a generic plan for prepared statements (PostgreSQL plan_cache_mode, SQL Server sniffing, Oracle bind peeking) and fix skew-driven regressions."
sources:
  - https://www.postgresql.org/docs/current/sql-prepare.html#SQL-PREPARE-NOTES
  - https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-PLAN-CACHE-MODE
  - https://learn.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide#parameter-sensitivity
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generic vs custom plans for prepared statements

Prepared statements save parse/plan time, but one plan may be reused for every parameter value.
When data is skewed (one tenant with 90% of rows), the reused plan is wrong for some values.

## PostgreSQL
- The first **5** executions of a prepared statement get a **custom plan** (planned with actual
  parameter values). After that, the planner compares the average custom-plan cost with a
  **generic plan** (planned without values); if the generic plan is not much more expensive, it
  switches to it permanently for that session's statement.
- Symptom: a query is fast the first few times from the app, then suddenly slow; or fast in psql
  (literals) and slow via the driver (prepared). `EXPLAIN EXECUTE stmt(...)` shows `$1` in
  conditions for a generic plan.
- Control:
  ```sql
  SET plan_cache_mode = force_custom_plan;     -- auto (default) | force_generic_plan | force_custom_plan
  ALTER ROLE app SET plan_cache_mode = force_custom_plan;   -- or per function: ALTER FUNCTION ... SET
  ```
  Custom plans cost planning time each execution; use per role/function, not globally, for
  skew-sensitive queries.
- Drivers: JDBC `prepareThreshold` (default 5 server-side prepares), PgBouncer transaction
  mode prepared statement support (1.21+) affects which statements are prepared.

## SQL Server
Parameter sniffing: the plan compiled for the **first** parameter value is cached and reused.
Fixes per query: `OPTION (RECOMPILE)`, `OPTIMIZE FOR (@p = value)` / `OPTIMIZE FOR UNKNOWN`,
Query Store plan forcing or hints, and on SQL Server 2022 (compat 160) **Parameter Sensitive
Plan optimization** caches several plan variants by cardinality range automatically.

## Oracle
Bind peeking at hard parse, plus **adaptive cursor sharing**: the cursor is marked
bind-sensitive; after a bad execution it becomes bind-aware and gets child cursors for different
selectivity ranges (`v$sql.is_bind_aware`). SQL plan baselines stabilize a known-good plan.

## MySQL
Server-side prepared statements re-optimize on each execution for most queries (no shared plan
cache), so the issue mostly does not arise; the cost is optimization time.

## Diagnosing
Capture the slow execution's actual plan (auto_explain with `log_analyze`, Query Store, ASH/
SQL Monitor), compare with the plan for a "typical" value, and check statistics/histograms on
the skewed column.

## Verify
After the change, the problematic parameter values use an appropriate plan (check EXPLAIN for
the specific value and the app's p99 latency), without a large rise in planning/CPU time.

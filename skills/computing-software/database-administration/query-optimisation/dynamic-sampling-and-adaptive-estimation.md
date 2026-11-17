---
id: computing-software.database-administration.query-optimisation.dynamic-sampling-and-adaptive-estimation
name: dynamic-sampling-and-adaptive-estimation
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, dynamic-sampling, adaptive-query-processing, adaptive-joins, query-statistics, cardinality-feedback]
level: practitioner
status: draft
description: "Use runtime and adaptive estimation: Oracle dynamic sampling and adaptive plans, SQL Server adaptive joins and memory grant feedback, and their PostgreSQL/MySQL analogues."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/optimizer-statistics-concepts.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing
  - https://www.postgresql.org/docs/current/runtime-config-query.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic sampling and adaptive estimation

## Oracle
- **Dynamic statistics (sampling)**: at parse time, sample blocks to estimate selectivity for complex predicates or tables without stats. `OPTIMIZER_DYNAMIC_SAMPLING` (default 2: tables without stats); level 11 = automatic (optimizer decides). Per query: `/*+ DYNAMIC_SAMPLING(t 4) */`.
- **Adaptive plans** (12c+): the plan contains alternative join methods; a statistics collector at runtime switches nested loops ↔ hash join after seeing actual rows. `DBMS_XPLAN.DISPLAY_CURSOR(format => '+ADAPTIVE')` shows inactive branches.
- **SQL plan directives** and statistics feedback record misestimates and trigger dynamic sampling or extended stats later. Check `DBA_SQL_PLAN_DIRECTIVES`. `OPTIMIZER_ADAPTIVE_STATISTICS` is FALSE by default in 12.2+/19c (it caused parse overhead).

## SQL Server (Intelligent Query Processing)
| Feature | Compat level | What it does |
|---|---|---|
| Adaptive joins | 140 (batch), 150 row-store via batch mode on rowstore | Chooses hash or nested loop after reading the build input |
| Interleaved execution | 140 | Real cardinality for multi-statement TVFs |
| Memory grant feedback | 140 batch / 150 row / 160 percentile + persisted | Corrects over/under grants across executions |
| Table variable deferred compilation | 150 | Real table variable row counts |
| CE feedback, DOP feedback | 160 | Adjusts model assumptions / parallelism |
| Parameter Sensitive Plan optimization | 160 | Multiple plans per parameter range |
Enable by raising database compatibility level (test with Query Store A/B first); disable a single feature with database scoped configurations if it regresses.

## PostgreSQL
No runtime plan switching. Analogues:
- Generic vs custom plans for prepared statements (`plan_cache_mode`).
- Extension `pg_hint_plan` with `Rows()` hints to correct estimates.
- Bitmap scans and hash joins degrade more gracefully than nested loops under misestimates; `enable_nestloop` testing in sessions shows sensitivity.

## MySQL
Histograms and `optimizer_switch` flags (`hash_join`, `subquery_to_derived`); no adaptive execution in community MySQL. Index dives for range estimates (`eq_range_index_dive_limit`) are effectively runtime sampling.

## Caveats
Adaptive features hide estimation problems rather than fixing them; extra parse/sampling time hurts high-frequency short queries. Fix root causes (stats, predicates) for hot queries.

## Verify
Plans show the adaptive operator choosing the expected branch (SQL Server actual plan `Adaptive Join` with `Actual Join Type`; Oracle `+ADAPTIVE` output), and runtime variance across parameter values shrinks.

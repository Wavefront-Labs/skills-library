---
id: computing-software.database-administration.postgresql.jit-compilation-settings
name: jit-compilation-settings
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-jit, jit-above-cost, llvm, query-performance, oltp-latency]
level: practitioner
status: docs-checked
description: "Decide when PostgreSQL LLVM JIT helps or hurts, read JIT timing in EXPLAIN ANALYZE, and tune jit_above_cost or disable JIT for OLTP latency."
sources:
  - https://www.postgresql.org/docs/18/jit.html
  - https://www.postgresql.org/docs/18/jit-decision.html
  - https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-JIT-ABOVE-COST
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JIT compilation settings

PostgreSQL (built `--with-llvm`) can JIT-compile expressions and tuple deforming for expensive queries. The docs say JIT is beneficial primarily for long-running CPU-bound (usually analytical) queries; for short queries the compilation overhead often exceeds the saving, so it can **hurt** OLTP queries whose cost estimate is inflated.

## Settings
| GUC | Default | Meaning |
|---|---|---|
| `jit` | on | master switch (takes effect at plan and execution time) |
| `jit_above_cost` | 100000 | plan cost above which JIT is used (-1 disables) |
| `jit_inline_above_cost` | 500000 | also inline short functions and operators (-1 disables) |
| `jit_optimize_above_cost` | 500000 | also apply expensive optimisations (-1 disables) |

The decisions are made at plan time from the estimated cost. They can be changed per session with `SET`, and per role or database with `ALTER ROLE` / `ALTER DATABASE ... SET`.

## Diagnose
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
-- footer:
-- JIT:
--   Functions: 3
--   Options: Inlining false, Optimization false, Expressions true, Deforming true
--   Timing: Generation 1.259 ms (Deform 0.000 ms), Inlining 0.000 ms, Optimization 0.797 ms, Emission 5.048 ms, Total 7.104 ms
-- Execution Time: 7.416 ms
```
(The footer is the form shown in the PostgreSQL JIT chapter.) If JIT Total is a large share of execution time, JIT is the problem. The `pg_stat_statements` view also has `jit_functions` and `jit_generation_time` columns (plus inlining, optimization and emission counters) to find which statements pay it.

## Fixes (pick the narrowest)
```sql
ALTER ROLE app_oltp SET jit = off;                -- OLTP service account
ALTER DATABASE reporting SET jit_above_cost = 500000;
-- cluster-wide, if nothing benefits:
ALTER SYSTEM SET jit = off; SELECT pg_reload_conf();
```
Raising the thresholds is better than off when the same database has real analytical queries. Fix the root cause too: a hugely over-estimated plan cost (stale stats, bad row estimates) is what triggers JIT on a query that returns 10 rows.

## Verify
```sql
SHOW jit; SELECT pg_jit_available();   -- true only if a JIT compiler is available AND jit = on
```

## Gotchas
- `pg_jit_available()` false where you expected JIT: either `jit` is off or no JIT implementation is available (for example a server built without `--with-llvm`).
- With prepared statements and a generic plan, the JIT decision follows the settings in effect at prepare time, not at execution time.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): JIT chapter (beneficial mainly for long-running CPU-bound queries, cost-based plan-time decisions with the three thresholds, effect of prepared statements and generic plans, `jit = off` effective at plan and execution time, sample EXPLAIN ANALYZE JIT footer), the four settings and their defaults (`jit` on, 100000, 500000, 500000, -1 disables), `pg_jit_available()` semantics and the `pg_stat_statements` JIT columns. Corrected: `pg_jit_available()` is also false when `jit` is off. Removed the 50-500 ms figure, the PG12 and PG15 version gates, the packaging remark and the parallel-worker remark, which the documentation does not give.
Method: documentation only; no commands were run.

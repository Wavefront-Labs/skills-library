---
id: computing-software.database-administration.query-optimisation.statistics-and-cardinality-estimation
name: statistics-and-cardinality-estimation
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, statistics, cardinality-estimation, query-planner, histogram, selectivity, correlated-columns, parameter-sniffing, skewed-data, cost-based-optimizer]
level: advanced
status: draft
description: "Diagnose bad query plans caused by stale, sampled, or correlated-column statistics misleading the cost-based optimizer, across Postgres, MySQL, and SQL Server."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statistics and cardinality estimation — why the optimizer picked that plan

**Goal:** recognize when a bad plan is a statistics problem rather than a missing
index, and know the specific blind spots every cost-based optimizer shares.

## 1. The optimizer's whole job rests on row-count estimates
A cost-based optimizer picks join order, join algorithm (nested loop vs. hash vs.
merge), and access path (index vs. scan) based on **estimated** rows at each step,
not actual rows — it never runs the query to find out. Every estimate error
compounds through the plan: misjudge the first join's output size and every
downstream join-algorithm choice built on that number is likely wrong too. This is
why a query can look "obviously" fine (there's an index, the SQL is clean) and
still perform badly — the plan was optimal for the estimate, just not for reality.

## 2. Staleness: the obvious case
Statistics (histograms, distinct-value counts, null fractions) are snapshots,
refreshed on a schedule or threshold, not live. A bulk load, mass delete, or any
large change between refreshes leaves the optimizer planning against
stale numbers. Symptom: a query regresses right after a big data change with no
code deploy. Fix: explicit stats refresh (`ANALYZE` in Postgres/MySQL, `UPDATE
STATISTICS` in SQL Server, `DBMS_STATS.GATHER_*` in Oracle) after large batch
operations rather than waiting for the automatic threshold.

## 3. Sampling error on skewed data
Most engines sample rather than scan every row when gathering statistics (for
speed on large tables). A sampled histogram can misrepresent a skewed
distribution — e.g. 95% of rows have `status = 'closed'` but a 1% sample happens
to catch a disproportionate share of the rare value, making it look more common
than it is (or the reverse). Symptom: a predicate on a known-skewed column gets a
wildly wrong row estimate despite "fresh" stats. Fix: increase sample size/
statistics target for that specific column (Postgres `ALTER TABLE ... ALTER
COLUMN ... SET STATISTICS n`; SQL Server `WITH FULLSCAN`) rather than globally,
since full-scan stats gathering is expensive at scale.

## 4. Correlated columns: the blind spot sampling can't fix
Optimizers generally assume columns are **independent** when estimating combined
selectivity — `WHERE city = 'Boston' AND zip_code = '02108'` gets its estimate as
if the two predicates were unrelated, multiplying their individual selectivities,
even though in reality the zip code almost entirely determines the city (their
combination is far more selective — or in some cases, far less — than that
product suggests). This produces systematically wrong estimates that no amount of
re-sampling the individual columns fixes, because the problem is the independence
assumption itself. Fixes: multi-column statistics (Postgres `CREATE STATISTICS ...
(dependencies, ndistinct)`, SQL Server multi-column stats, Oracle extended
statistics) teach the optimizer the actual correlation.

## 5. Parameter sniffing / plan caching compounds this
A cached plan was optimized for the parameter value used on its first execution;
if that value's cardinality was atypical (a customer with 1 order vs. one with
1 million), every subsequent call with a *different* value reuses a plan tuned for
the wrong shape. Symptom: the same query text is fast for some parameter values and
catastrophically slow for others. Mitigations are engine-specific (SQL Server
`OPTIMIZE FOR`/recompile hints, Postgres's custom vs. generic plan choice after 5
executions, Oracle adaptive cursor sharing/bind-aware peeking) — diagnosing this as
"parameter sniffing" rather than "random slowness" is the key step.

## 6. Reading the symptom, not just the plan
Compare the plan's **estimated** rows at each node against the **actual** rows (
`EXPLAIN ANALYZE` in Postgres/MySQL 8, `SET STATISTICS PROFILE`/actual execution
plans in SQL Server, `DBMS_XPLAN.DISPLAY_CURSOR` with actuals in Oracle). A large
estimated-vs-actual gap at a specific node is the direct pointer to which
statistic is wrong — don't guess which table's stats are stale, let the plan tell
you.

## Verify
- [ ] A regressed query's plan was compared estimated-vs-actual rows per node before any index change was attempted.
- [ ] Large batch loads/deletes are followed by an explicit stats refresh, not left to the automatic threshold.
- [ ] Known-skewed columns have increased sample size/statistics target, not the table default.
- [ ] Predicates on correlated columns were checked against multi-column/extended statistics support in the engine.
- [ ] A query with wildly inconsistent latency across calls was checked for parameter-sniffing/plan-cache reuse before being called "flaky."

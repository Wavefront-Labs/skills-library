---
id: computing-software.data-engineering.data-quality.source-to-target-reconciliation
name: source-to-target-reconciliation
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-testing, source-target-reconciliation, control-totals, row-count-checks, financial-reconciliation, audit-balance-control, tolerance]
level: practitioner
status: gated
description: "Reconcile every pipeline run against its source: control totals captured at extract, layer-by-layer counts and sums, tolerances, reconciliation tables, and alerting on breaks."
sources:
  - https://github.com/GoogleCloudPlatform/professional-services-data-validator
  - https://docs.getdbt.com/blog/audit-helper-for-migration
  - https://www.dama.org/cpages/body-of-knowledge
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Source-to-target reconciliation

**Goal:** prove, every run, that what arrived in the warehouse equals what the source had — and catch silent losses (dropped rows, filtered joins, truncated files) the day they happen.

## 1. Audit-balance-control pattern
- **Audit**: record each run (run id, source, window, start/end, status).
- **Balance**: control totals at extract and at each layer; compare.
- **Control**: rules for what happens on a break (stop publish, alert, quarantine).

## 2. Capture control totals at the source
At extract time, in the same query/snapshot as the data:
```sql
SELECT COUNT(*) AS n_rows, SUM(amount) AS sum_amount, COUNT(DISTINCT order_id) AS n_keys,
       MIN(updated_at) AS min_ts, MAX(updated_at) AS max_ts
FROM orders WHERE updated_at > :lo AND updated_at <= :hi;
```
For files: trailer records or manifests from the producer (row count, hash totals). Store in `ops.recon_controls(run_id, layer, dataset, metric, value)`.

## 3. Compare per layer
(Ran on DuckDB 1.5 with a 10 vs 9 row break and a 5.5 vs 5.5 sum with 0.01 tolerance: returns BREAK and OK as intended.)
```sql
WITH s AS (SELECT metric, value FROM ops.recon_controls WHERE run_id = :run AND layer = 'source'),
     t AS (SELECT metric, value FROM ops.recon_controls WHERE run_id = :run AND layer = 'silver')
SELECT s.metric, s.value AS source_value, t.value AS target_value,
       t.value - s.value AS diff,
       CASE WHEN ABS(t.value - s.value) <= COALESCE(tol.abs_tolerance, 0) THEN 'OK' ELSE 'BREAK' END AS status
FROM s JOIN t USING (metric) LEFT JOIN ops.recon_tolerances tol ON tol.metric = s.metric;
```
- Layers: source → bronze (should be exact) → silver (expected differences: dedup, filtering — reconcile with **explained** differences: `bronze_rows = silver_rows + duplicates_removed + rows_quarantined`) → gold (aggregates: sums per business key/date equal silver).
- Financial data: sums to the cent per currency and per day, debit = credit totals.

## 4. Tolerances
- Exact for counts and money in batch loads.
- Small tolerances only with a reason (float rounding, known late arrivals within window). Store them in a table with owner and justification — not hard-coded in SQL.

## 5. When things break
- Block downstream publishing for the affected dataset (dbt test severity error / pipeline gate) for critical data; warn for the rest.
- The break report shows which metric, layer, and the first layer where the difference appears — that's where to look.
- Recurring explained differences become new categories in the balance equation.

## 6. Tools
dbt tests comparing to a control table (`dbt_utils.equality`, custom tests), Soda cross-dataset checks, Great Expectations, Google DVT for cross-database column/row validation, audit_helper in dbt (tool names not re-checked here (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] Every critical pipeline writes control totals for source and each layer per run.
- [ ] Deleting one row from a bronze test load produces a BREAK.
- [ ] Silver/bronze differences are fully explained by recorded dedup/quarantine counts.

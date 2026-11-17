---
id: computing-software.data-engineering.etl-pipeline-design.data-diffing-between-versions
name: data-diffing-between-versions
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, pipeline-testing, data-diff, regression-testing, dbt-audit-helper, datafold, reladiff, except-all, change-review]
level: practitioner
status: gated
description: "Diff the output of a changed pipeline against the current version: keyed row diffs, column-level mismatch summaries, EXCEPT queries, audit_helper and hash-based diff tools."
sources:
  - https://github.com/dbt-labs/dbt-audit-helper
  - https://github.com/erezsh/reladiff
  - https://docs.datafold.com/data-diff/what-is-data-diff
  - https://docs.snowflake.com/en/sql-reference/operators-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data diffing between pipeline versions

**Goal:** before merging a transformation change, know exactly which rows and columns change in the output, and confirm only the intended ones do.

Run here on DuckDB 1.5.6 with small tables (`COUNT_IF`, `EXCEPT`, `EXCEPT ALL`, `IS DISTINCT FROM`, `FULL OUTER JOIN ... USING` all ran). Findings: `EXCEPT` is distinct (two copies of a row versus one copy showed no difference; `EXCEPT ALL` showed it), and `a.amount <> b.amount` missed a NULL-to-value change that `IS DISTINCT FROM` caught. Caveat: in the keyed diff below, an added or removed row has NULL on one side, so `IS DISTINCT FROM` also counts it in every `*_changed` column; filter to keys present on both sides (`WHERE a.order_id IS NOT NULL AND b.order_id IS NOT NULL`) for the column counts. The dbt audit_helper macros, Datafold, Snowflake `COUNT_IF` and reladiff were not run: reladiff 0.6.0 does not support SQLite and its DuckDB connector failed to find a table in a test file (gated: unconfirmed, source is paywalled or blocked).

## 1. Build both versions side by side
- Prod output: `analytics.fct_orders`. Candidate: build the PR into `ci_pr_123.fct_orders` (dbt `--target ci`, or run the job with a different output schema).
- Same inputs for both: point the candidate at prod sources (dbt `--defer --state prod-artifacts`) or freeze inputs with clones / time travel.

## 2. Quick set diff (any warehouse)
```sql
-- rows only in prod / only in candidate
SELECT 'removed' AS side, * FROM (SELECT * FROM analytics.fct_orders EXCEPT SELECT * FROM ci_pr_123.fct_orders)
UNION ALL
SELECT 'added', * FROM (SELECT * FROM ci_pr_123.fct_orders EXCEPT SELECT * FROM analytics.fct_orders);
```
`EXCEPT` is distinct by default; use `EXCEPT ALL` where supported if duplicates matter. Floats need rounding first or every row differs.

## 3. Keyed diff with column breakdown
```sql
WITH a AS (SELECT * FROM analytics.fct_orders), b AS (SELECT * FROM ci_pr_123.fct_orders)
SELECT
  COUNT_IF(a.order_id IS NULL)                      AS added,
  COUNT_IF(b.order_id IS NULL)                      AS removed,
  COUNT_IF(a.amount IS DISTINCT FROM b.amount)      AS amount_changed,
  COUNT_IF(a.status IS DISTINCT FROM b.status)      AS status_changed
FROM a FULL OUTER JOIN b USING (order_id);
```
`IS DISTINCT FROM` treats NULL = NULL as equal; plain `<>` silently skips NULL changes.

dbt shortcut (audit_helper):
```sql
{{ audit_helper.compare_all_columns(
     a_relation=ref('fct_orders'), b_relation=api.Relation.create(database='prod', schema='analytics', identifier='fct_orders'),
     primary_key='order_id') }}
```
`compare_relations` gives a summary of matched / a-only / b-only percentages.

## 4. Big tables and cross-database
- Hash-based tools (reladiff, the open-source successor of data-diff; Datafold cloud) checksum key ranges and recurse only into mismatching segments — fast across databases (e.g. Postgres source vs Snowflake target).
```bash
reladiff "postgresql://<user>@<host>/db" public.orders "snowflake://<account>/DB/PUBLIC?warehouse=WH" ORDERS -k order_id -c amount -c status
```
- Sample by date partition for a fast PR check, full diff before release.

## 5. Reading the result
- Expected change only (e.g. new column, fixed rounding) → paste the summary in the PR.
- Unexpected removed rows usually mean a join changed from LEFT to INNER or a filter moved.
- Many tiny numeric diffs → type/precision change (DECIMAL scale, float aggregation order).

## Verify
- [ ] Both versions read identical inputs.
- [ ] Diff summary (added/removed/changed per column) is attached to the PR.
- [ ] Every changed column is one the PR intended to change.

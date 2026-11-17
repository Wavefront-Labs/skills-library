---
id: computing-software.data-engineering.dbt.choosing-view-table-or-ephemeral
name: choosing-view-table-or-ephemeral
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-materializations, view-vs-table, ephemeral-models, materialized-table, materialized-view-dbt, cte-injection, build-cost]
level: practitioner
status: docs-checked
description: "Pick dbt materializations deliberately: view vs table vs ephemeral vs incremental by query cost, freshness and reuse; ephemeral CTE pitfalls; and a default per layer."
sources:
  - https://docs.getdbt.com/docs/build/materializations
  - https://docs.getdbt.com/best-practices/materializations/1-guide-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing view, table, or ephemeral

**Goal:** each model costs the least total compute (build + all reads) while staying fresh enough.

## Options
| Materialization | Build | Read cost | Use when |
|---|---|---|---|
| `view` | `create view as` on each run | Slow to query if the view does significant work or sits on other views | Models that do little transformation (renaming, recasting); the dbt default |
| `table` | Rebuilt with `create table as` on every run | Fast to query | Models queried by BI tools, and slower transformations used by many downstream models |
| `incremental` | Inserts or updates only rows since the last run | Fast to query | Event-style data when `dbt run` becomes too slow; do not start with incremental |
| `ephemeral` | Not built: interpolated as a CTE (prefixed `__dbt__cte__`) into dependents | n/a | Very light transformations early in the DAG, used by one or two models, never queried directly |
| `materialized_view` | Created and maintained in the target database | Table-like speed with view-like freshness | Platform-supported near-real-time needs, similar use cases to incremental models |

## Defaults that work for most projects
```yaml
models:
  acme:
    staging:      {+materialized: view}
    marts:        {+materialized: table}
```
Start with views and change a model to another materialization only when you notice performance problems; move to `incremental` when `dbt run` becomes too slow.

## Ephemeral pitfalls
- You cannot select directly from an ephemeral model; overuse makes queries harder to debug; it does not support model contracts.
- Operations (macros called with `dbt run-operation`) cannot `ref()` ephemeral nodes.

## View pitfalls
- Views that do significant transformation, or are stacked on other views, are slow to query; use a table for models BI tools query.

## Measure, then choose
Compare build time and cost against how often the model is read, using your warehouse query history.

## Verify
- [ ] Every mart queried by BI is a table or incremental.
- [ ] No ephemeral model is used by more than one or two downstream models.
- [ ] Table builds that make `dbt run` too slow are reviewed for incremental conversion.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt materializations page: view is the default, behaviour and advice for view, table, incremental, ephemeral (CTE prefix `__dbt__cte__`, cannot select directly, run-operation cannot ref ephemeral nodes, no model contracts, use for one or two dependents) and materialized_view; staging as views from the staging guide. Removed unconfirmed claims about default intermediate layer, CTE recomputation, view breakage and numeric thresholds.

Method: documentation only; no commands were run.

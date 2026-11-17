---
id: computing-software.data-engineering.dbt.dbt-clone
name: dbt-clone
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-clone, zero-copy-clone, ci-environment, blue-green-deployment, state-flag, shallow-clone, snowflake, databricks, bigquery]
level: advanced
status: docs-checked
description: "Use dbt clone to copy prod relations into a dev/CI schema via zero-copy clones (or views): state selection, incremental CI, blue-green deploys, and adapter differences."
sources:
  - https://docs.getdbt.com/reference/commands/clone
  - https://docs.getdbt.com/reference/node-selection/defer
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dbt clone

**Goal:** materialise prod relations into another schema cheaply, so CI/dev work starts from real tables (especially incremental models) without rebuilding them.

## Command
```bash
dbt clone --select state:modified+,config.materialized:incremental --state prod-state --target ci
dbt build -s state:modified+ --defer --state prod-state --target ci
```
For each selected node, dbt creates in the target schema:
- a **zero-copy clone** where the data platform supports it (Snowflake, Databricks or BigQuery) and the model exists as a table in the source environment,
- otherwise a **pointer view** (`select * from` the source object).
By default `dbt clone` does not recreate pre-existing relations in the target; `--full-refresh` overrides this. Raise `--threads` to run independent clone statements in parallel.

## Why clone instead of defer alone
- Incremental models in CI: cloning your modified incremental models first avoids costly full-refresh builds on warehouses with zero-copy cloning.
- Deferral works only inside dbt; `dbt clone` creates real warehouse objects, so BI tools and notebooks can test changes against them.

## Blue-green pattern
The documentation lists blue/green continuous deployment as a use case on warehouses with zero-copy table cloning.

## Gotchas
- Without zero-copy support (or when the source is not a table), dbt creates a pointer view (`select * from` the source object).
- `--state` points at artifacts of the state to clone from; use the latest production manifest.

## Verify
- [ ] After clone, `select count(*)` on a cloned incremental model equals prod.
- [ ] The cloned relations exist in the target schema before the CI build runs.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt clone reference: clone materialization (zero-copy on Snowflake, Databricks, BigQuery for tables, otherwise a pointer view), no recreation of existing relations without `--full-refresh`, `--threads`, `--state`, use cases (blue/green deployment, cloning production into development, incremental models in CI, BI testing), and when to prefer deferral. Removed the unconfirmed version gate, Snowflake schema-swap recipe, write-divergence and privilege claims.

Method: documentation only; no commands were run.

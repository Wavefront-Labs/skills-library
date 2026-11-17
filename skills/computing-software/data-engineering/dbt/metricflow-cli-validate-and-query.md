---
id: computing-software.data-engineering.dbt.metricflow-cli-validate-and-query
name: metricflow-cli-validate-and-query
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-semantic-layer, metricflow, mf-cli, dbt-sl-cli, validate-configs, query-metrics, semantic-manifest]
level: practitioner
status: docs-checked
description: "Develop dbt Semantic Layer metrics locally with the MetricFlow CLI (mf / dbt sl): validate configs, list metrics and dimensions, query with filters, and inspect generated SQL."
sources:
  - https://docs.getdbt.com/docs/build/metricflow-commands
  - https://docs.getdbt.com/docs/build/validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MetricFlow CLI: validate and query

**Goal:** iterate on semantic models and metrics with fast feedback before they reach BI tools.

## Two CLIs
- **Self-hosted:** `python -m pip install "dbt-metricflow[dbt-snowflake]"` (use your adapter's extra) -> `mf` commands.
- **dbt platform (CLI / IDE):** `dbt sl ...` commands, run with your account credentials.
Commands below show `mf`; `dbt sl` has equivalents (`dbt sl query`, `dbt sl list metrics`, `dbt sl validate`).

## Validate
```bash
dbt parse                                  # builds target/semantic_manifest.json
mf validate-configs                        # semantic + warehouse validations
mf validate-configs --skip-dw              # skip warehouse queries (fast, CI on PR)
```
`dbt sl validate` checks your local semantic manifest, including uncommitted changes.

## Explore
```bash
mf list metrics
mf list dimensions --metrics revenue,order_count
mf list entities --metrics revenue
mf list dimension-values --metrics revenue --dimension customer__region
```

## Query
```bash
mf query --metrics revenue,order_count --group-by metric_time__month,customer__region \
  --where "{{ Dimension('customer__region') }} = 'EMEA'" \
  --start-time 2026-01-01 --end-time 2026-09-30 --order-by -revenue --limit 20
mf query --metrics revenue --group-by metric_time__week --explain       # show generated SQL (dbt sl: --compile)
mf query --saved-query weekly_kpis
mf query --metrics revenue --group-by metric_time --csv out.csv        # --csv: mf only, not dbt sl
```
Group-by syntax: `entity__dimension`; time dimensions take a granularity suffix, e.g. `metric_time__month`.

## Debugging tips
- `--explain` (and `--show-dataflow-plan`) reveals join paths; unexpected fan-out means an entity relationship is wrong (`primary` vs `foreign`/`unique`).
- `--where` filters on dimensions use the `{{ Dimension('entity__dim') }}` Jinja form (and `TimeDimension('metric_time', 'week')` for time).

## CI
```bash
dbt parse && mf validate-configs --skip-dw
```
Run full DW validation on merge to main with a warehouse connection.

## Gotchas
- Local `mf` runs against your warehouse: the semantic models' underlying tables must exist in the target schema.

## Verify
- [ ] `mf validate-configs` passes in CI.
- [ ] Key metrics queried via CLI match a trusted SQL reference for one period.

## Checked

2026-11-01. Confirmed against the dbt MetricFlow commands page (`mf`/`dbt sl` equivalents, install command, list commands, `--metrics`, `--group-by`, `--where` with `Dimension()`/`TimeDimension()`, `--start-time`, `--end-time`, `--limit`, `--order-by`, `--saved-query`, `--explain`/`--compile`, `--csv` self-hosted only) and the validation page (`dbt sl validate`, `mf validate-configs`). Fixed: `--order` is `--order-by`. Removed: join-path error, agg_time_dimension, --defer and version-alignment notes, validation check list, granularity list.

Method: documentation only; no commands were run.

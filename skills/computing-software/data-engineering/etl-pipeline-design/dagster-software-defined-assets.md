---
id: computing-software.data-engineering.etl-pipeline-design.dagster-software-defined-assets
name: dagster-software-defined-assets
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, orchestration, software-defined-assets, dagster, asset-checks, partitions, declarative-automation, io-managers]
level: practitioner
status: gated
description: "Build asset-based pipelines in Dagster: @asset definitions and dependencies, partitions and backfills, asset checks, resources, and declarative automation instead of cron DAGs."
sources:
  - https://docs.dagster.io/guides/build/assets
  - https://docs.dagster.io/guides/build/partitions-and-backfills
  - https://docs.dagster.io/guides/test/asset-checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagster software-defined assets

**Goal:** model the pipeline as the data assets it produces (tables, files, models) with lineage, partitions and quality checks, and let the orchestrator decide what needs materialising.

## Assets and dependencies
```python
import dagster as dg

@dg.asset(group_name="sales", kinds={"snowflake"})
def raw_orders(context: dg.AssetExecutionContext, snowflake: SnowflakeResource) -> dg.MaterializeResult:
    n = load_orders(snowflake)
    return dg.MaterializeResult(metadata={"rows": n})

@dg.asset(deps=[raw_orders])
def clean_orders(snowflake: SnowflakeResource):
    run_sql(snowflake, "create or replace table clean.orders as select ... from raw.orders")

defs = dg.Definitions(assets=[raw_orders, clean_orders],
                      resources={"snowflake": SnowflakeResource(account=dg.EnvVar("SF_ACCOUNT"), ...)})
```
Dependencies come from `deps` or function parameters (with IO managers passing data). Integrations generate assets from other tools: `dagster-dbt` (every dbt model becomes an asset), `dagster-airbyte`, `dagster-fivetran`, `dagster-sling`. (gated: unconfirmed, source is paywalled or blocked)

## Partitions and backfills
```python
daily = dg.DailyPartitionsDefinition(start_date="2025-01-01", timezone="UTC")

@dg.asset(partitions_def=daily)
def daily_events(context: dg.AssetExecutionContext):
    day = context.partition_key           # '2026-10-17'
    load_day(day)
```
Backfill a range from the UI or CLI (`dagster asset materialize --select daily_events --partition-range 2026-09-01...2026-09-30`); Dagster tracks which partitions are materialised and their status. Backfill policies can run a range in one run (`BackfillPolicy.single_run()`) for efficiency.

## Asset checks
```python
@dg.asset_check(asset=clean_orders, blocking=True)
def orders_pk_unique(snowflake: SnowflakeResource) -> dg.AssetCheckResult:
    dupes = scalar(snowflake, "select count(*) from (select order_id from clean.orders group by 1 having count(*) > 1)")
    return dg.AssetCheckResult(passed=dupes == 0, metadata={"dupes": dupes})
```
`blocking=True` stops downstream assets in the same run when the check fails (WAP-like gate). dbt tests surface as asset checks via dagster-dbt.

## Automation
- Schedules on asset jobs (`dg.define_asset_job` + `dg.ScheduleDefinition`).
- Sensors for external events.
- **Declarative automation:** `automation_condition=dg.AutomationCondition.eager()` (materialise when upstream updates) or `.on_cron("0 6 * * *")` on assets; Dagster evaluates conditions continuously. Freshness policies/checks express SLAs.

## Gotchas
- Code locations run as separate processes; heavy imports at module load slow the UI and daemon (same "top-level code" rule as Airflow).
- Partition mapping between assets with different partitioning (daily -> monthly) needs explicit `PartitionMapping`.
- IO managers are convenient for small data; for warehouse tables prefer assets that run SQL in place and return metadata.

## Verify
- [ ] Asset graph in the UI shows full lineage including dbt models.
- [ ] Failed blocking check prevents downstream materialisation in a test run.

## Checked

2026-11-02

- Confirmed: Dagster assets and asset-checks guide pages were fetched.
- Removed or gated: The partitions-and-backfills page was a stub; API names (AutomationCondition.eager, BackfillPolicy.single_run, MaterializeResult, EnvVar) and the integration package names are gated, confirm in the Dagster API reference for your version.

Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.apache-airflow.conditional-asset-schedules
name: conditional-asset-schedules
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-assets, asset-expressions, conditional-dataset-scheduling, assetortimeschedule, datasetortimeschedule, asset-alias, data-aware-scheduling]
level: advanced
status: docs-checked
description: "Combine Airflow asset triggers: AND/OR asset expressions, AssetOrTimeSchedule for data-or-deadline runs, and AssetAlias for assets decided at runtime."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/asset-scheduling.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/timetable.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/assets.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional asset schedules

**Goal:** express "run when A and (B or C) have updated" or "run when data arrives, but at least daily", without sensors.

## Logical expressions
```python
from airflow.sdk import Asset, dag
orders = Asset("s3://lake/silver/orders/")
refunds = Asset("s3://lake/silver/refunds/")
fx_ecb = Asset("s3://lake/ref/fx_ecb/")
fx_vendor = Asset("s3://lake/ref/fx_vendor/")

@dag(schedule=(orders & refunds) & (fx_ecb | fx_vendor), catchup=False)
def revenue_mart(): ...
```
- `&` = all of the assets must have been updated; `|` = any one of them. A plain list `[a, b]` means all assets must have been updated at least once since the DAG last ran.
- If one asset is updated several times before the others update, the DAG still runs once for that condition (asset-triggered runs are created per event by default; see `batch_asset_events` for batching).

## Data or time
```python
from airflow.sdk import AssetOrTimeSchedule, CronTriggerTimetable

@dag(schedule=AssetOrTimeSchedule(
        timetable=CronTriggerTimetable("0 7 * * *", timezone="UTC"),
        assets=(orders & refunds)),
     catchup=False)
def daily_finance(): ...
```
Runs on the 07:00 schedule **and** whenever the asset condition is met; the scheduled runs and asset-triggered runs are created independently, so a report is produced even if upstream stalls (the task should then detect staleness and alert). To gate the scheduled run on asset readiness instead, use `AssetAndTimeSchedule`, which creates a scheduled run only after the assets are ready and creates no asset-triggered runs.

## Asset aliases: assets known only at runtime
```python
from airflow.sdk import AssetAlias, Asset, task
@task(outlets=[AssetAlias("partner-feeds")])
def ingest(*, outlet_events):
    for p in discovered_partners():
        outlet_events[AssetAlias("partner-feeds")].add(Asset(f"s3://lake/partners/{p}/"))
# downstream DAGs can depend on the alias; Airflow triggers them when events are added to it
```

## Gotchas
- OR schedules can trigger a consumer before the other inputs are fresh; the task must handle partially updated inputs.
- When a DAG is triggered by several assets there may be several events per asset; the DAG author decides whether to process all new data or each event (`triggering_asset_events`).
## Verify
- [ ] Triggering only `orders` does not run `revenue_mart`; triggering `orders`, `refunds`, and either FX source does.
- [ ] `daily_finance` runs at 07:00 even with no upstream events.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the `&` and `|` operators and list semantics, `AssetOrTimeSchedule` and `AssetAndTimeSchedule` behaviour with the `airflow.sdk` imports, `AssetAlias` with `outlet_events` and dependence on the alias, per-event runs and `batch_asset_events`, and the `triggering_asset_events` caveat (asset-scheduling.rst, timetable.rst, assets.rst). Removed the 2.9 and 2.10 version tags, the Airflow 2 class name, the paused-consumer claim and the per-consumer evaluation claim, which are not documented.

Method: documentation only; no commands were run.

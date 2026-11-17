---
id: computing-software.data-engineering.apache-airflow.asset-decorator-definitions
name: asset-decorator-definitions
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-3, asset-decorator, airflow-assets, asset-centric, multi-asset, data-aware-scheduling, asset-dependencies]
level: practitioner
status: verified
description: "Define asset-centric pipelines in Airflow 3 with the @asset and @asset.multi decorators: one-asset DAGs, upstream asset inputs, schedules and when to use classic DAGs instead."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/assets.html
  - https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-75+New+Asset-Centric+Syntax
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @asset decorator definitions (Airflow 3)

**Goal:** write "this function produces this data asset" and let Airflow derive the DAG, task and data-aware schedule.

## One asset = one DAG with one task
```python
from airflow.sdk import asset

@asset(schedule="@daily", uri="s3://lake/raw/orders/")
def raw_orders(context):
    ds = context["ds"]
    extract_orders_to_s3(ds)

@asset(schedule=raw_orders)                    # runs when raw_orders is updated
def clean_orders(context, raw_orders):          # parameter named after upstream asset = inlet
    # the docs say a parameter named after an asset declares an inlet; it is not the data
    transform("s3://lake/raw/orders/", "s3://lake/clean/orders/")
```
- The function name becomes the asset name and the DAG id.
- `schedule` accepts cron/timetables, another asset, or asset expressions (`raw_orders & raw_customers`).
- Declaring an upstream asset as a function parameter adds it as an inlet (`self`, `context` and `outlet_events` are reserved names Airflow fills in). Read the data yourself from its URI.

## Multiple assets from one task
```python
from airflow.sdk import Asset, asset

@asset.multi(schedule="@hourly", outlets=[Asset("s3://lake/dim/customers/"), Asset("s3://lake/dim/accounts/")])
def crm_dims(context):
    load_crm()
```

## Attaching metadata to the event
```python
from airflow.sdk import Metadata

@asset(schedule="@daily")
def daily_revenue(self):
    rows = compute()
    yield Metadata(self, {"row_count": rows})   # stored on the asset event (extra)
```
(`def daily_revenue(self)`: `self` is the asset itself.) Alternatively set `context["outlet_events"][self].extra = {...}`; extra must be JSON-serialisable. Downstream tasks read `context["inlet_events"][asset][-1].extra`.

## When classic @dag is better
- Several tasks with retries/branches per step: use a normal DAG with `outlets=[Asset(...)]` on the producing task.
- Mixed producer DAGs: assets updated by different tasks of one DAG.
`@asset` shines for small, single-step, data-defined nodes and readable lineage in the Assets view.

## Gotchas
- Asset updates are recorded only when the task **succeeds** (failed or skipped tasks produce no update), whether or not data changed. Raise `AirflowSkipException` if nothing was produced to avoid triggering consumers.
- URIs are case-sensitive plain strings and the docs describe no normalisation: keep one spelling in a shared module. Observed with task-sdk `Asset`: `Asset("s3://lake/x/").uri` is `s3://lake/x` (trailing slash stripped), but `name` defaults to the raw string, so `Asset("s3://lake/x") == Asset("s3://lake/x/")` is False.
- Assets are Airflow-internal events; external writers must post asset events through the Airflow REST API (see the API reference for the asset-events endpoint) to trigger consumers.

## Verify
- [ ] Assets view shows the dependency edge raw_orders -> clean_orders.
- [ ] Successful raw_orders run creates an asset event and queues one clean_orders run.

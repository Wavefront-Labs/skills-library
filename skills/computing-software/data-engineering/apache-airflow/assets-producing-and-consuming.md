---
id: computing-software.data-engineering.apache-airflow.assets-producing-and-consuming
name: assets-producing-and-consuming
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-assets, airflow-datasets, data-aware-scheduling, outlets, inlets, asset-events, asset-uri, airflow-3]
level: practitioner
status: verified
description: "Trigger Airflow DAGs from data updates: declare Asset outlets on producer tasks, schedule consumers on assets, read triggering asset events, and Airflow 2 Dataset equivalents."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html
  - https://airflow.apache.org/docs/apache-airflow/2.10.5/authoring-and-scheduling/datasets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assets: producing and consuming (data-aware scheduling)

**Goal:** downstream DAGs run when the data they need has been updated, instead of guessing with time offsets or sensors.

Airflow 3 calls them **Assets** (`airflow.sdk.Asset`); Airflow 2.x called them **Datasets** (`airflow.datasets.Dataset`; the upgrade guide maps it to `airflow.sdk.Asset`). Same model.

## Producer
```python
from airflow.sdk import dag, task, Asset
orders_silver = Asset("s3://lake/silver/orders/", extra={"owner": "orders-team"})   # URI is an identifier

@dag(schedule="@hourly", catchup=False)
def load_orders():
    @task(outlets=[orders_silver])
    def write_silver():
        ...                    # on success, Airflow records an asset event
    write_silver()
load_orders()
```
An asset event is emitted only when the task **succeeds** (failed or skipped tasks produce no update), regardless of whether data changed. Raise `AirflowSkipException` if nothing was written to avoid spurious downstream runs.

## Consumer
```python
@dag(schedule=[orders_silver], catchup=False)
def build_orders_mart():
    @task
    def build(**ctx):
        for ev in ctx["triggering_asset_events"][orders_silver]:      # docs iterate the mapping with .items()
            print(ev.source_dag_id, ev.source_run_id, ev.extra)
    build()
build_orders_mart()
```
- With several assets in the list, the consumer runs once **all** have been updated since its last run (AND).
- Multiple producer updates before the consumer runs are coalesced into one consumer run (it sees all events).
- Producers can attach metadata to the event: yield `Metadata(asset, {...})` (`from airflow.sdk import Metadata`) from the task, or set `outlet_events[asset].extra = {...}` (JSON-serialisable).

## Naming
Asset URIs/names are identifiers, not checked against storage (the SDK strips a trailing slash from `uri` but keeps it in the default `name`, so spell them identically). Agree on a scheme (`s3://bucket/path`, `postgres://host/db/schema/table`, or Airflow 3 `Asset(name="orders_silver", uri=...)`), and keep it in a shared module imported by both DAGs to avoid typos creating disconnected assets.

## Logical date
Asset-triggered runs have no meaningful schedule interval (check the current docs for what `logical_date` holds in them). Tasks must derive what to process from the asset events or from state (watermarks), not from `ds`.

## Verify
- [ ] UI Assets view shows the producer -> asset -> consumer graph.
- [ ] A producer success creates an asset event and queues a consumer run.
- [ ] A producer run that writes nothing does not trigger the consumer (skip path tested).

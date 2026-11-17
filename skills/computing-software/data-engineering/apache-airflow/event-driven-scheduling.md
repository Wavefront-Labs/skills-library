---
id: computing-software.data-engineering.apache-airflow.event-driven-scheduling
name: event-driven-scheduling
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, event-driven-scheduling, asset-watchers, messagequeuetrigger, sqs, rest-api-trigger, external-asset-events, airflow-3, data-aware-scheduling]
level: advanced
status: docs-checked
description: "Start Airflow runs from external events: Airflow 3 AssetWatcher with message-queue triggers (SQS/Kafka), posting asset events or DAG runs via the REST API, and dedup/idempotency."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/event-scheduling.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/asset-scheduling.rst
  - https://github.com/apache/airflow/blob/main/providers/common/messaging/docs/triggers.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/api_fastapi/core_api/openapi/v2-rest-api-generated.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event-driven scheduling

**Goal:** react to things that happen outside Airflow (file landed, message published, upstream system finished) within seconds, without polling sensors.

## Option 1: Asset watchers (Airflow 3.0+)
A watcher runs a trigger in the **triggerer**; each event it yields creates an asset event, which schedules consumer DAGs.
```python
from airflow.sdk import Asset, AssetWatcher, dag, task
from airflow.providers.common.messaging.triggers.msg_queue import MessageQueueTrigger

trigger = MessageQueueTrigger(scheme="sqs", sqs_queue="https://sqs.eu-west-1.amazonaws.com/<acct>/landing-events")
landing = Asset("landing_files", watchers=[AssetWatcher(name="landing_sqs", trigger=trigger)])

@dag(schedule=[landing])
def process_landing():
    @task
    def handle(triggering_asset_events):
        for ev in triggering_asset_events[landing]:
            print(ev.extra["payload"])     # message payload
    handle()
process_landing()
```
- Triggers run in the triggerer, so it must be running; install the `common.messaging` provider plus the provider for your queue. `MessageQueueTrigger` takes a mandatory `scheme` (`sqs`, `kafka`, `redis+pubsub`, ...) and queue-specific parameters, and uses the provider's default connection id (for SQS, `aws_default`).
- Only triggers that inherit from `BaseEventTrigger` can be used for event-driven scheduling; not every deferrable trigger qualifies.

## Option 2: REST API from the event source
Create a DAG run directly:
```bash
curl -X POST "https://<AIRFLOW>/api/v2/dags/process_landing/dagRuns" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"logical_date": null, "conf": {"path": "s3://landing/x.csv"}}'
```
Or create an **asset event** (`POST /api/v2/assets/events` with `asset_id` and `extra`) so the normal asset schedule logic applies.

## Design rules
- Queues and retrying callers can deliver an event more than once: make the DAG idempotent per payload (dedupe on object key or etag).
- Bursts: asset-triggered DAGs create one run per event by default; set `batch_asset_events=True` on the timetable (or `[scheduler] batch_asset_events`) to consume queued events together in one run. Per-event run creation respects `max_active_runs`. REST `dagRuns` calls create one run each; use `max_active_runs` and pools to protect downstream systems.
- Auth: use a service account/token with only the permissions to trigger that DAG.
- Keep a periodic reconciliation run (e.g. hourly listing) as a safety net for lost events.

## Verify
- [ ] Publishing a test message creates an asset event and a DAG run.
- [ ] Sending the same event twice produces no duplicate side effects.
- [ ] Triggerer health monitored (it is now on the critical path).

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: asset watchers added in Airflow 3.0, `Asset(watchers=[AssetWatcher(name=..., trigger=...)])`, `MessageQueueTrigger(scheme="sqs", sqs_queue=...)` as in the provider system test, `triggering_asset_events[asset]` with the payload under `extra["payload"]`, the `BaseEventTrigger` requirement, `POST /api/v2/dags/{dag_id}/dagRuns` with `logical_date` and `conf`, `POST /api/v2/assets/events` with `asset_id` and `extra` (OpenAPI spec), and per-event runs versus `batch_asset_events`. Removed the Airflow 2.x endpoint note, the S3-Lambda example caller and the claim that events coalesce into one run by default, which is wrong.

Method: documentation only; no commands were run.

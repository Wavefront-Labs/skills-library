---
id: computing-software.data-engineering.apache-airflow.triggerer-ha-and-capacity
name: triggerer-ha-and-capacity
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, triggerer-capacity, triggerer, deferrable-operators, high-availability]
level: advanced
status: docs-checked
description: "Run the Airflow triggerer in HA and tune capacity: multiple replicas, the capacity setting, blocked event loop warnings, and metrics to watch for deferrable workloads."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html
  - https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#triggerer
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/metrics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triggerer HA and capacity

**Goal:** keep deferred tasks resuming promptly as the number of concurrent sensors/deferrable operators grows.

## How it works
Each `airflow triggerer` process runs an asyncio loop holding up to `capacity` triggers. Triggers are assigned to live triggerers; if one dies (missed heartbeats), its triggers are reassigned to others. Running 2+ triggerers gives HA and more capacity with no extra config.

## Capacity
- `[triggerer] capacity` (default 1000; the older `default_capacity` name is deprecated since 3.0) or `airflow triggerer --capacity 500`.
- Effective limit is CPU and the quality of trigger code, not the number: one blocking trigger stalls all others in that process.
- Run more than one triggerer replica (for example through the Helm chart) and size resources to the trigger workload.

## Blocked event loop
Log warning `Triggerer's async thread was blocked for N seconds, likely by a badly-written trigger` means a trigger does sync I/O (`requests`, `time.sleep`, a sync SDK call). Fix the trigger: use `aiohttp`/async SDKs, `asyncio.sleep`, or `asgiref.sync.sync_to_async` for unavoidable sync calls.

## Metrics
- `triggers.running` (per triggerer host): approaching capacity -> add replicas.
- `triggers.blocked_main_thread`: any non-zero is a bug in a trigger.
- `triggers.failed`, `triggers.succeeded`.
- `triggerer_heartbeat` / health endpoint for liveness.

## Gotchas
- No triggerer running = deferrable tasks stay `deferred` until timeout. Check `airflow jobs check --job-type TriggererJob`.
- Triggers must be serializable and cheap to re-create; the triggerer can restart them elsewhere.
- Trigger logs go to the task log of the deferred TI, so remote logging must be configured for the triggerer too.

## Verify
Defer 2x your expected peak of a test sensor and confirm resume latency stays low, and `triggers.blocked_main_thread` stays zero.

## Checked

2026-10-28. Confirmed in the Airflow configuration reference, CLI reference and metrics page: `[triggerer] capacity` default 1000, `default_capacity` deprecated since 3.0, `airflow triggerer --capacity`, `airflow jobs check --job-type TriggererJob`, metrics `triggers.running`, `triggers.blocked_main_thread`, `triggers.failed`, `triggers.succeeded`, `triggerer_heartbeat`. Removed: the `triggerer.replicas` value, the `serialize()` detail and the seconds figure.
Method: documentation only; no commands were run.

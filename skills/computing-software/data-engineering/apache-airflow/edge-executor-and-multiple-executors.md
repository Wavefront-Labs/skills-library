---
id: computing-software.data-engineering.apache-airflow.edge-executor-and-multiple-executors
name: edge-executor-and-multiple-executors
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, edgeexecutor, multiple-executors, hybrid-executor, remote-workers]
level: sme
status: docs-checked
description: "Run Airflow tasks on several executors at once (Celery plus Kubernetes) and on remote sites with the EdgeExecutor, including config syntax and per-task routing."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html#using-multiple-executors-concurrently
  - https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge executor and multiple executors

**Goal:** mix execution models in one deployment: fast Celery workers for small tasks, Kubernetes pods for isolated heavy tasks, edge workers in a remote network.

## Multiple executors
The executor page has a section "Using Multiple Executors Concurrently" (configuration, aliases, per-task routing); follow it for the exact syntax. The first configured executor is the default for tasks and DAGs that do not specify one.

## EdgeExecutor (provider apache-airflow-providers-edge3)
The provider handles edge workers on remote sites over HTTP(S). Take the executor path, `[edge]` settings and the worker start command from the provider's Edge Worker Deployment page, and keep Airflow and provider versions aligned between server and edge workers.

## Gotchas
- DAG code and dependencies must be present on every executor's workers; version drift between edge workers and the server breaks task execution.
- Secure the edge API endpoint (auth, TLS) as it dispatches code to remote workers.
- `CeleryKubernetesExecutor` and `LocalKubernetesExecutor` were replaced by the multiple-executor configuration in Airflow 3.

## Verify
Task instance details show the executor; edge workers show up in the provider's Edge UI plugin.

## Checked

2026-10-28. Confirmed against: executor concepts page (default executor, section list), Airflow 3 upgrade guide (hybrid executors replaced), edge3 provider index (edge workers on remote sites via HTTP(S), Edge UI Plugin, Edge Worker Deployment). Removed (not confirmable in the fetched pages): ini syntax with aliases, 2.10 gate, [edge] settings, worker CLI flags, per-executor parallelism claim, pull-model and NAT detail.

Method: documentation only; no commands were run.

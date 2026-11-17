---
id: computing-software.data-engineering.prefect.worker-start-and-polling
name: worker-start-and-polling
category: computing-software
field: data-engineering
product: prefect
tags: [worker, prefetch, heartbeat, install-policy, work-pool]
level: practitioner
status: docs-checked
description: "Start Prefect workers with prefect worker start, flags, install policies, prefetch and polling defaults, heartbeat status and required environment."
sources:
  - https://docs.prefect.io/v3/concepts/workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a worker that polls a pool and submits flow runs.

Minimum: `prefect worker start -p <pool>`. Types: `process`, `kubernetes`, `docker`, `ecs`, `cloud-run-v2`, `vertex-ai`, `azure-container-instance`, `coiled`; a worker only polls pools of its type. Most need a package (`prefect-kubernetes`, `prefect-docker`, `prefect-aws`, `prefect-gcp`, `prefect-azure`, `prefect-coiled`).

Flags: `--name/-n`, `--pool/-p`, `--work-queue/-q` (repeatable; omitted polls all; missing queues are created), `--type/-t` (inferred from the pool if omitted; creates the pool with defaults if it does not exist), `--prefetch-seconds`, `--run-once`, `--limit/-l` (max concurrent runs), `--with-healthcheck`, `--install-policy`.

Environment: set `PREFECT_API_URL`; on Cloud the `PREFECT_API_KEY` must belong to a user or service account with the `Worker` role. Prefect must be installed where flows run.

Timing: prefetch default 10 s (`PREFECT_WORKER_PREFETCH_SECONDS`); poll default 15 s (`PREFECT_WORKER_QUERY_SECONDS`). Statuses `ONLINE` and `OFFLINE`; three missed heartbeats mark a worker offline (about 90 s; `PREFECT_WORKER_HEARTBEAT_SECONDS`).

`--install-policy`: `always`, `if-not-present`, `never`, `prompt` (default; non-interactive behaves as `never`). For production use prebuilt images with pinned tags.

## Checked

2026-11-08. Worker types and packages, every listed flag with its short form, queue and pool auto-creation, API URL and Worker role requirement, prefetch default 10 s, poll default 15 s, ONLINE and OFFLINE status with the three-missed-heartbeats (90 s) rule, and the four install policies with the non-interactive prompt behaviour confirmed against the Workers page.

Method: documentation only; no commands were run.

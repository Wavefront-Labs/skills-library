---
id: computing-software.data-engineering.prefect.work-pools-and-queues
name: work-pools-and-queues
category: computing-software
field: data-engineering
product: prefect
tags: [work-pool, work-queue, priority, push-pool, managed-pool]
level: practitioner
status: docs-checked
description: "Prefect work pool types (hybrid, push, managed), work queue priority and concurrency limits, and queue status rules."
sources:
  - https://docs.prefect.io/v3/concepts/work-pools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose a pool type and set queue priorities.

Pool types:
- Hybrid: a worker in your infrastructure submits runs.
- Push: no worker; runs go to your serverless provider.
- Managed: no worker; runs go to Prefect-managed infrastructure.

Infrastructure types on Prefect Cloud: Process, AWS ECS, Azure Container Instances, Docker, Google Cloud Run, Cloud Run V2, Vertex AI, Kubernetes, plus Cloud Run Push, ECS Push, ACI Push, Modal Push, Coiled and Prefect Managed. A self-hosted server lists the first eight only.

Work queues:
- Every pool has a queue named `default`, used when none is specified.
- Priority is a unique positive integer; lower number means higher priority, `1` highest. Adding a queue does not change others' ranks.
- Each queue can have its own concurrency limit and is also bound by the pool's global limit.
- Priority sets submission order, waterfall from highest to lowest; it matters when limits block some runs.

Example from the page: `low` priority 10 no limit; `high` priority 5 limit 3; `critical` priority 1 limit 1.

Queue status:
- `READY`: a worker polled in the last 60 seconds
- `PAUSED`: accepts no new work until unpaused (UI)
- `NOT_READY`: after unpausing unless polled within 60 seconds

## Checked
2026-11-08. Confirmed against the Work pools concept page: hybrid, push and managed types, Cloud and self-hosted infrastructure type lists, default queue, priority rules, queue concurrency and the pool global limit, the low, high and critical example, and READY, PAUSED and NOT_READY with the 60 second window. Nothing removed.
Method: documentation only; no commands were run.

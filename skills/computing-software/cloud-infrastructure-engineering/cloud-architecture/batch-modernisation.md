---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.batch-modernisation
name: batch-modernisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, batch-modernisation, batch-jobs, cron-migration, aws-batch, step-functions, event-driven-batch, job-scheduling]
level: practitioner
status: draft
description: "Modernise legacy batch (cron, mainframe JCL, ETL windows) to cloud: managed schedulers, containerised jobs, idempotent steps, event-driven triggers and job observability."
sources: ["https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html", "https://learn.microsoft.com/azure/architecture/guide/technology-choices/batch", "https://cloud.google.com/run/docs/create-jobs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modernising batch jobs

## Steps
1. **Inventory** jobs: schedule, dependencies, runtime, input/output, SLAs (must finish by),
   failure handling, owners. Scheduler exports (cron, Control-M, Autosys, JCL) are the source.
2. **Classify**: can it become event-driven (process each file/record on arrival) instead of
   nightly? Many nightly windows exist only because of old constraints.
3. **Target platform**:
   - Short containerised jobs: Cloud Run jobs, Container Apps jobs, ECS scheduled tasks, Kubernetes CronJobs.
   - Large parallel compute: AWS Batch, Azure Batch, Google Batch.
   - Multi-step dependencies: Step Functions, Logic Apps/Durable Functions, Workflows, Airflow.
   - Data transforms: managed Spark / SQL in the warehouse.
4. **Make steps idempotent and restartable** (checkpoints, write to staging then swap).
5. **Scheduling**: managed schedulers (EventBridge Scheduler, Cloud Scheduler) with timezones and
   DST handled explicitly.
6. **Observability**: job success/failure metrics, duration vs SLA, alerts on missed runs
   (dead-man's switch).
7. **Cost**: spot capacity for fault-tolerant jobs.

## Gotchas
- Implicit dependencies (job B assumes A's file exists) break when moved; model them.
- DST: jobs scheduled at 02:30 local run twice or not at all.
- Kubernetes CronJob `concurrencyPolicy` default Allow can overlap runs.

## Verify
- [ ] Parallel run against legacy outputs matches for a full business cycle.
- [ ] Missed-run alert tested.

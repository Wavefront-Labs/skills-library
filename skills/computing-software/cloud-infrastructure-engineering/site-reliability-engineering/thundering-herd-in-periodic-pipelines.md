---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.thundering-herd-in-periodic-pipelines
name: thundering-herd-in-periodic-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, data-pipelines, pipeline-thundering-herd, cron-jitter, scheduling, moire-load]
level: practitioner
status: docs-checked
description: "Prevent thundering herds in periodic pipelines and cron jobs: bounded worker counts, sane retry logic, staggered start times and concurrency caps on shared dependencies."
sources: ["https://sre.google/sre-book/data-processing-pipelines/", "https://sre.google/sre-book/distributed-periodic-scheduling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thundering herd in periodic pipelines

**Goal:** stop every job starting at the same instant and overwhelming shared systems.

## How it happens (SRE Book, Data Processing Pipelines)
- In a large periodic pipeline, thousands of workers can start work immediately at each cycle. Too many workers,
  misconfigured workers, or faulty retry logic overwhelm the servers, the shared cluster services and the network.
- With no retry logic, work dropped on failure is never redone (a correctness problem); naive or poor retry logic
  compounds the overload.
- Engineers with limited pipeline experience tend to add more workers when a job misses its deadline, which
  amplifies the problem.
- Overlapping pipelines on a shared resource produce a Moire load pattern (see
  `moire-load-and-staggered-schedules`).

## Mitigations
1. Cap and size the worker count deliberately; do not add workers just because a run is late.
2. Retries that are implemented and non-naive: delay between attempts and randomise it so failed jobs do not retry
   together. The cron chapter discusses the same herd problem for distributed cron.
3. Stagger start times across jobs so they do not share a start instant.
4. Concurrency caps per shared dependency.
5. For continuous data, use continuous processing instead of a periodic pipeline (the book's recommendation).
6. Monitor dependency load over time; plotting shared-resource usage reveals herds and overlaps.

## Verify
- [ ] Shared dependency load graph shows no sharp spikes at schedule boundaries; post-outage catch-up runs are rate-limited.

## Checked
2026-11-01. Confirmed against the SRE Book chapters "Data Processing Pipelines" (thundering herd paragraph, retry logic, adding workers, continuous pipelines, Moire load pattern) and "Distributed Periodic Scheduling with Cron" (cross-reference).
Removed: Jenkins hash syntax, Kubernetes CronJob statements, Airflow pools, full-jitter formula and the AWS Builders' Library source (not read), advice on popular schedule times.
Method: documentation only; no commands were run.

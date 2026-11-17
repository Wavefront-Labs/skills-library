---
id: computing-software.ai-ml-engineering.mlops.pipeline-step-caching-idempotency-and-backfills
name: pipeline-step-caching-idempotency-and-backfills
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, pipeline-orchestration, step-caching, idempotency, backfills, cache-keys, kubeflow-pipelines]
level: practitioner
status: draft
description: "Design ML pipeline steps that cache safely and backfill correctly: cache keys from code, params and data versions, idempotent writes, disabling cache, and point-in-time backfills."
sources:
  - https://www.kubeflow.org/docs/components/pipelines/user-guides/core-functions/caching/
  - https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-caching.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#backfill
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Step caching, idempotency and backfills

**Goal:** re-runs skip work that hasn't changed, never reuse stale results, and historical backfills produce what would have been produced at the time.

## What a cache key must include
1. Code version (container image digest or code hash) - not a mutable tag like `latest`.
2. All parameters.
3. Input data **versions** (dataset snapshot ID, partition, commit), not just paths. `s3://bucket/features/latest/` as an input makes caching wrong by construction.
4. Library/environment version if it can change outputs.

Platform behaviour:
- **Kubeflow Pipelines:** caches a task when component spec + inputs match a previous execution; disable per task with `task.set_caching_options(False)`. Inputs that are paths to mutable data defeat it.
- **SageMaker Pipelines:** `CacheConfig(enable_caching=True, expire_after="P7D")`; key from step arguments.
- **Prefect/Dagster:** explicit cache keys (`cache_key_fn`) or asset code versions / data versions.

## Don't cache
Steps with side effects (deploy, notify, write to a serving table), steps reading "now" or external APIs, and evaluation steps whose holdout gets refreshed.

## Idempotent steps
- Write outputs to deterministic, versioned locations: `s3://ml/features/date=2026-10-01/run=<id>/` then atomically publish (rename/manifest/pointer update).
- Overwrite a partition rather than append rows - a retried append duplicates data.
- Use upserts keyed by entity+timestamp for tables.
- Seed randomness from parameters so a rerun is reproducible.

## Backfills
- Parameterise every step by the logical date (data interval), never wall-clock time.
- Use point-in-time data for that date: features as of the date, the model version that was live then (for score backfills), labels available by then (for training backfills).
- Run backfills with bounded concurrency so they don't starve daily jobs (`max_active_runs`, separate queue).
- Record which code version produced each backfilled partition.

## Verify
- [ ] Rerun with identical inputs hits the cache; changing data version misses it.
- [ ] Killing and retrying a step mid-write leaves no duplicates or partial outputs.
- [ ] Backfilled outputs for a past date match the original outputs where those exist.

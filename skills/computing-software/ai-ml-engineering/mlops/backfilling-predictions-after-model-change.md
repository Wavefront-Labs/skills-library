---
id: computing-software.ai-ml-engineering.mlops.backfilling-predictions-after-model-change
name: backfilling-predictions-after-model-change
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, batch-inference, prediction-backfill, model-versioning, idempotent-pipelines, data-reprocessing]
level: practitioner
status: draft
description: "Backfill historical predictions after a model or feature change: versioned prediction tables, idempotent partitions, point-in-time features and validation before swap."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#backfill
  - https://docs.dagster.io/guides/build/partitions-and-backfills
  - https://docs.delta.io/latest/delta-batch.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backfilling predictions after model changes

**Triggers:** new model version must be compared over history, downstream reports need consistent scores, a feature bug corrupted past predictions, or a new consumer needs history.

## Rules
1. **Never overwrite the old version in place.** Store predictions partitioned by `model_version` and `date` (or a separate table per version). Old and new coexist until consumers move.
2. **Point-in-time features.** Rescore each historical date with features as they were known on that date (feature store point-in-time joins, Delta/Iceberg time travel), not today's values - otherwise the backfill leaks the future and looks better than reality.
3. **Idempotent partitions.** Each task writes exactly one `(model_version, date)` partition with overwrite semantics (`replaceWhere` in Delta, `INSERT OVERWRITE PARTITION`). Reruns and retries cannot duplicate.
4. **Orchestrate as partitions.** Airflow `airflow dags backfill -s 2025-01-01 -e 2025-12-31 score_dag` (or `max_active_runs` limits), Dagster partitioned assets with backfill launches. Throttle concurrency so the backfill does not starve production jobs or hit model-server rate limits.

## Validate before swapping
- Row counts per date equal source counts.
- Score distribution per date vs old version (PSI); large jumps on specific dates point at feature gaps.
- Business metric replay where labels exist (AUC by month old vs new).
- Spot-check entities across both versions.

## Swap
Point consumers at the new version through a view or alias (`CREATE OR REPLACE VIEW predictions AS SELECT ... WHERE model_version = 'v8'`). Announce the change with the date range, expected shifts and the rollback (revert the view). Keep the old partitions for a defined retention period.

## Cost control
Estimate rows x inference cost before starting; for LLM-based scoring use batch APIs (50% discount) and checkpoint progress per partition so failures resume rather than restart.

## Verify
- [ ] Backfill rerun for one date leaves counts unchanged (idempotence).
- [ ] Point-in-time check: features for a 2025 date contain no values updated after that date.
- [ ] Rollback by view revert tested.

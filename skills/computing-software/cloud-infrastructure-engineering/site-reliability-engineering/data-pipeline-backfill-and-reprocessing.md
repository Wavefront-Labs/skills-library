---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.data-pipeline-backfill-and-reprocessing
name: data-pipeline-backfill-and-reprocessing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, data-pipelines, pipeline-backfill, reprocessing, idempotency, data-correctness]
level: advanced
status: docs-checked
description: "Plan and run pipeline backfills and reprocessing safely: idempotent outputs, partitioned reruns, capacity isolation from live runs, validation and communication."
sources: ["https://sre.google/workbook/data-processing/", "https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#backfill", "https://sre.google/sre-book/data-processing-pipelines/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline backfill and reprocessing

**Goal:** fix historical output (bug fix, new field, late data) without breaking live processing or consumers.

## Preconditions
- **Idempotent, partitioned outputs**: each run writes a complete partition with overwrite semantics, or uses merge keys; rerunning yields the same result (the Workbook's idempotent mutation pattern).
- Deterministic code given the same inputs and config version; inputs still retained for the range.
- Versioned code/config so you know which version produced which partition.

## Plan
1. Define the range, the reason, and the expected output change (row counts, metrics).
2. Estimate cost and duration (per-partition runtime x partitions / parallelism).
3. **Isolate capacity**: separate queue/pool or lower priority so live (freshness SLO) runs are not starved by the backfill.
4. Decide write strategy: in-place overwrite, or write to a new table/version and swap after validation (safer).
5. Notify downstream consumers: their caches/aggregates may need recompute.

## Run (Airflow example)
Airflow documents backfill as running a Dag for a historical period, from the UI (Dag Details, Trigger, Backfill: date range, reprocess behavior, max active runs) or the CLI:
```bash
airflow backfill create --dag-id DAG_ID --from-date START_DATE --to-date END_DATE \
    --reprocess-behavior failed --max-active-runs 3
```
It re-runs the Dag's instances for every interval in the range; cap `--max-active-runs` to protect live runs.

## Validate
- Row counts and checksums per partition vs expectations; spot-check business metrics before/after.
- Data quality tests on the rewritten partitions.
- Compare old and new outputs side by side when writing to a new version.

## Verify
- [ ] All partitions in range report success; validation diff matches the expected change; live pipeline freshness SLO unaffected during the backfill.

## Checked
2026-11-01. Confirmed in the Airflow Dag run page (backfill definition, UI form fields, `airflow backfill create` options, catchup) and the SRE Workbook Data Processing chapter (idempotent mutations, data reprocessing after failure). Removed: Airflow 2 command, dbt and Great Expectations specifics, the attribution of the freshness warning to the Workbook, the example partition name.
Method: documentation only; no commands were run.

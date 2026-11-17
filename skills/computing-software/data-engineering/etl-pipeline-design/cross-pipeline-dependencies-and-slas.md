---
id: computing-software.data-engineering.etl-pipeline-design.cross-pipeline-dependencies-and-slas
name: cross-pipeline-dependencies-and-slas
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, orchestration, pipeline-dependencies, data-aware-scheduling, sla, freshness-slo, critical-path, sensors, cross-team-dependencies]
level: advanced
status: draft
description: "Coordinate dependencies between pipelines owned by different teams: data-aware triggers instead of clock guesses, freshness SLOs, critical-path analysis, and SLA miss handling."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html
  - https://docs.dagster.io/guides/automate/declarative-automation
  - https://docs.getdbt.com/reference/resource-properties/freshness
  - https://sre.google/sre-book/service-level-objectives/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-pipeline dependencies and SLAs

**Goal:** downstream pipelines start when upstream data is actually ready, and everyone knows when published data is late and why.

## 1. Stop chaining by clock
"Upstream usually finishes by 03:00, so schedule downstream at 04:00" fails on every slow day and wastes an hour every normal day. Replace with a readiness signal:
| Mechanism | Example |
|---|---|
| Data-aware scheduling | Airflow Assets (Datasets) — producer task declares `outlets=[Asset("s3://.../orders")]`, consumer DAG `schedule=[Asset(...)]` |
| Asset-based automation | Dagster declarative automation (`AutomationCondition.eager()`), asset sensors |
| Table update triggers | Databricks table-update triggers; Snowflake streams + tasks |
| Completion markers | `_SUCCESS` files or a `ops.dataset_versions` table with (dataset, partition, ready_at) that consumers poll |
| Sensors (last resort) | `ExternalTaskSensor` / `S3KeySensor` in `mode="reschedule"` or deferrable, with timeout |
A shared readiness table works across tools and teams:
```sql
INSERT INTO ops.dataset_ready (dataset, partition_date, ready_at, run_id)
VALUES ('silver.orders', DATE '2026-10-16', current_timestamp(), :run_id);
```

## 2. Map the critical path
- Build the lineage graph from source to each SLA-bearing output (dbt manifest + orchestrator metadata, or OpenLineage).
- For each node record typical and p95 duration and start time; the critical path is the longest chain to the deadline.
- Optimise the critical path only: parallelise, start earlier (incremental), move heavy non-critical work off it.

## 3. Freshness SLOs, not just job success
- Define per published dataset: "`gold.daily_revenue` for day D is available by 07:00 UTC on D+1, 99% of days."
- Measure from the data (`max(loaded_at)`, readiness table), not from job status — a successful job can publish stale data.
- dbt source freshness `warn_after`/`error_after`; Dagster freshness checks; a SQL alert on the readiness table.

## 4. Predict and handle misses
- Alert on **SLA at risk** early: if an upstream dependency hasn't landed by (deadline − downstream p95 duration), page the owner then — not at the deadline.
- Communicate in a status channel: which outputs are late, expected time, cause.
- Decide per output whether to publish partial data (with a flag) or hold.
- Track SLA attainment monthly per dataset; repeated misses → fix upstream or renegotiate the SLA.

## 5. Contracts between teams
Each cross-team dependency gets an owner, readiness signal, schema contract, SLA and change-notification process. Producer changes to schedules or schemas go through the same review as API changes.

## Verify
- [ ] No downstream pipeline depends on upstream purely by schedule offset.
- [ ] Each SLA dataset has a freshness check measured from the data.
- [ ] At-risk alerts fire before the deadline in a test where upstream is delayed.

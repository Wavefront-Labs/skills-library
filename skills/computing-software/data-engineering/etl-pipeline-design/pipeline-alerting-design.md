---
id: computing-software.data-engineering.etl-pipeline-design.pipeline-alerting-design
name: pipeline-alerting-design
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, pipeline-alerting, alert-fatigue, on-call, slo]
level: advanced
status: draft
description: "Design data pipeline alerting that people act on: alert on SLA impact not every failure, severity routing, deduplication, ownership, runbook links and alert reviews."
sources:
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://sre.google/workbook/alerting-on-slos/
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pipeline alerting design and alert fatigue

**Goal:** every alert is actionable, reaches the owner, and important problems are never buried in noise.

## Alert on symptoms consumers feel
- **Freshness/SLA**: "fct_orders not updated by 07:00" is what matters; an individual retry failing at 03:00 that later succeeds is not.
- **Correctness**: failed data tests on critical models, reconciliation mismatches.
- **Completeness**: volume anomalies (row count far below expected).
Infrastructure failures (task failed) become alerts only if they threaten an SLA or have no retry.

## Severity and routing
| Severity | Example | Route |
|---|---|---|
| P1 | exec dashboard / customer-facing data late or wrong | page on-call |
| P2 | internal mart late, will miss SLA in hours | team channel + ticket |
| P3 | warning tests, non-critical failures | daily digest |
Tag every pipeline/model with owner and criticality (dbt `meta.owner`, Airflow `owner`/tags) and route by tag.

## Reduce noise
- Retries with backoff before alerting; alert on final failure.
- Deduplicate: one incident per root cause (upstream source down -> one alert, not 40 downstream failures). Alert on the first failing node; suppress dependents.
- Auto-resolve when the next run succeeds; but log it.
- Mute windows for planned maintenance.

## Make alerts actionable
Each alert includes: what is affected (models, dashboards), since when, severity, owner, last success time, link to logs and the **runbook** for that pipeline.

## Review
Monthly: count alerts per pipeline, % actionable, time to acknowledge. Delete or downgrade alerts nobody acts on; add alerts for incidents users reported first.

## Verify
For the last month, more than 80% of pages led to an action, and no SLA breach was reported by users before an alert fired.

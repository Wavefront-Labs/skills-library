---
id: computing-software.ai-ml-engineering.mlops.data-quality-gates
name: data-quality-gates
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, data-quality-gates, data-validation, pipeline-gates, quarantine, great-expectations]
level: practitioner
status: draft
description: "Gate ML pipelines on data quality: blocking vs warning checks, severity tiers, quarantining bad batches, thresholds from history, alert routing and override procedures."
sources:
  - https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions
  - https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
  - https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Data quality gates that block pipelines

**Principle:** a model trained or scored on broken data is worse than a delayed model. Put explicit pass/fail gates between ingestion and training/scoring.

## Severity tiers
| Tier | Example checks | Action |
|---|---|---|
| Blocking | schema mismatch, required column missing, row count < 50% of expected, primary key duplicates, label leakage column present, null rate > hard limit on critical features | fail the pipeline step, page owner |
| Warning | distribution shift (PSI > 0.2), null rate moderately up, new category values | continue, alert, annotate the run |
| Info | minor drift, metadata changes | log only |

## Implementation pattern
```python
results = run_checks(batch)                      # GE checkpoint, pandera, TFDV, Deequ
blocking = [r for r in results if r.severity == "blocking" and not r.passed]
if blocking:
    move_to_quarantine(batch, reason=blocking)   # keep the data for debugging
    raise DataQualityError(blocking)             # orchestrator marks the task failed
```
- In Airflow/Kubeflow/SageMaker Pipelines, the gate is a step whose failure stops downstream training/scoring (or a ConditionStep).
- Quarantine: write failing batches to a separate location with the check report; never silently drop.
- Scoring pipelines: fall back to the last good predictions or a safe default instead of scoring garbage.

## Thresholds
- Derive from history: e.g. expected row count = median of last 30 runs, block below 50%, warn below 80%.
- Version thresholds with the pipeline code; review false alarms monthly and tune.

## Overrides
Provide a documented manual override (flag + approver recorded) for known-benign anomalies (holiday volume drop), so engineers do not disable checks under pressure.

## Verify
- [ ] Inject a broken batch in staging (dropped column, duplicate keys): pipeline halts, batch quarantined, alert received.

---
id: computing-software.ai-ml-engineering.mlops.model-monitoring-alerts-and-runbooks
name: model-monitoring-alerts-and-runbooks
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-alerting, model-monitoring, runbooks, alert-fatigue, on-call, incident-response]
level: practitioner
status: draft
description: "Turn model monitoring into actionable alerts: what to alert on, thresholds and windows, severity routing, alert-fatigue controls and runbooks with diagnosis and rollback steps."
sources:
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-interpreting-cloudwatch.html
  - https://cloud.google.com/vertex-ai/docs/model-monitoring/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Model monitoring alerts and runbooks

**Problem:** dashboards nobody watches and drift alerts that fire daily are both useless. Alerts must be rare, actionable and owned.

## Alert hierarchy
| Signal | Window | Severity |
|---|---|---|
| Serving errors / latency SLO burn | minutes | page |
| Input schema failures, null spikes on critical features | 15-60 min | page or high |
| Prediction distribution shift (positive rate, mean score) vs baseline | hours | high |
| Feature drift (PSI/JS) on top-importance features | daily | ticket |
| Performance drop once labels arrive | daily/weekly | ticket, review |
| Low-importance feature drift | daily | dashboard only |

## Thresholds without noise
- Baseline from a stable reference period; alert on sustained deviation (e.g. 3 consecutive windows) rather than single spikes.
- Weight drift by feature importance; ignore drift in features the model barely uses.
- Account for seasonality (compare to same weekday/last year) for traffic-shaped metrics.
- Review alert precision monthly: every alert should have led to an action or a threshold change.

## Routing
Owner per model (team + on-call rotation) in the model registry metadata; alerts carry model name, version, metric, link to dashboard and runbook.

## Runbook template
1. **Confirm:** is it real? Check upstream data pipeline status, recent deploys (model/feature code), traffic mix changes.
2. **Scope:** which segments/features; compare with last model version's shadow scores if available.
3. **Mitigate:** roll back to the previous model alias; switch to fallback rules; pause automated actions driven by scores.
4. **Fix:** repair data, retrain on recent data, or adjust threshold; document.
5. **Close:** post-incident note, update thresholds/tests to catch it earlier.

## Verify
- [ ] Each production model has owner, alert definitions and a runbook link in the registry; a test alert reaches on-call.

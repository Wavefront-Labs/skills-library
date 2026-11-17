---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alert-policy-multiple-conditions-and-combiners
name: alert-policy-multiple-conditions-and-combiners
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alerting, condition-combiners, and-with-matching-resource, multi-condition-alerts, alert-policies]
level: practitioner
status: docs-checked
description: "Build Cloud Monitoring alert policies with several conditions: OR, AND and AND_WITH_MATCHING_RESOURCE combiners, and replacing them with one PromQL condition."
sources: ["https://cloud.google.com/monitoring/alerts/concepts-indepth#combining-conditions", "https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies#ConditionCombinerType", "https://cloud.google.com/monitoring/promql/create-promql-alerts-console"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alert policy multiple conditions and combiners

## Combiners
| `combiner` | Fires when |
|---|---|
| `OR` | any condition is met (independent incidents per condition/time series) |
| `AND` | all conditions met, possibly by different resources |
| `AND_WITH_MATCHING_RESOURCE` | all conditions met **by the same resource** (same monitored resource labels) |

## Example: high CPU and high latency on the same VM
```yaml
displayName: vm-cpu-and-latency
combiner: AND_WITH_MATCHING_RESOURCE
conditions:
- displayName: cpu > 90%
  conditionThreshold:
    filter: resource.type="gce_instance" AND metric.type="compute.googleapis.com/instance/cpu/utilization"
    comparison: COMPARISON_GT
    thresholdValue: 0.9
    duration: 300s
    aggregations: [{alignmentPeriod: 60s, perSeriesAligner: ALIGN_MEAN}]
- displayName: app latency > 1s
  conditionThreshold:
    filter: resource.type="gce_instance" AND metric.type="custom.googleapis.com/<APP_LATENCY_METRIC>"
    comparison: COMPARISON_GT
    thresholdValue: 1000
    duration: 300s
    aggregations: [{alignmentPeriod: 60s, perSeriesAligner: ALIGN_PERCENTILE_95}]
notificationChannels: [projects/<P>/notificationChannels/<ID>]
```
```bash
gcloud alpha monitoring policies create --policy-from-file=policy.yaml
```

## Prefer one PromQL condition for complex logic
```promql
(avg_over_time(<METRIC_A>[5m]) > 0.9)
and on (<JOIN_LABEL>)
(<METRIC_B> > 1000)
```
Metric names and the join label are placeholders: use the PromQL names Metrics Explorer shows. One condition, explicit join keys, testable in Metrics Explorer; use the `conditionPrometheusQueryLanguage` condition type.

## Gotchas
- `AND` without matching resource can fire from unrelated resources: rarely what you want.
- An alerting policy can contain up to 6 conditions; split policies for clarity.
- A log-based policy takes only one condition, with combiner `OR`.

## Verify
- [ ] Load one VM CPU only: no incident; CPU and latency high on that VM: one incident naming it.

## Checked

2026-10-28. Confirmed against: Cloud Monitoring API v3 discovery document (combiner values OR, AND, AND_WITH_MATCHING_RESOURCE; MetricThreshold and PrometheusQueryLanguageCondition fields) and the alert-conditions page (up to 6 conditions per policy; one `OR` condition for log-based policies).

Removed or rewritten: the open/close timing claim, and the invented metric names in the example (now placeholders).

Method: documentation only; no commands were run.

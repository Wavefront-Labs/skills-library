---
id: computing-software.cloud-infrastructure-engineering.google-cloud.latency-slis-with-distribution-cut
name: latency-slis-with-distribution-cut
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, slo-monitoring, distribution-cut-sli, latency-sli, request-based-sli, service-monitoring-api]
level: practitioner
status: docs-checked
description: "Define latency SLOs in Cloud Monitoring with distributionCut request-based SLIs: picking distribution metrics, the range threshold, bucket boundaries, and checking SLI values."
sources: ["https://docs.cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/timeseries-selectors", "https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/services.serviceLevelObjectives", "https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/services.serviceLevelObjectives/create", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Latency SLIs with distribution cut

A `distributionCut` SLI counts values in a DISTRIBUTION time series that fall in a range
as good, over the total count. The time series must be DISTRIBUTION valued with DELTA or CUMULATIVE kind. `goal` must be above 0 and at most 0.9999, and `rollingPeriod` must be a whole number of days no larger than 30 days. "95% of requests faster than 300 ms over 28 days."

## SLO definition
```json
{
  "displayName": "checkout p95 < 300ms",
  "goal": 0.95,
  "rollingPeriod": "2419200s",
  "serviceLevelIndicator": {
    "requestBased": {
      "distributionCut": {
        "distributionFilter": "metric.type=\"<DISTRIBUTION_LATENCY_METRIC>\" resource.type=\"<RESOURCE_TYPE>\"",
        "range": {"min": 0, "max": 300}
      }
    }
  }
}
```
```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "https://monitoring.googleapis.com/v3/projects/<P>/services/checkout/serviceLevelObjectives?serviceLevelObjectiveId=latency-300" \
  -d @slo.json
```
Units follow the metric, so set `range` in the metric's unit.

## Good metric choices
Pick a built-in latency metric of your service from the Cloud Monitoring metrics list (load balancer or Cloud Run latency metrics are DISTRIBUTION valued), or a custom histogram exported to Monitoring as a DISTRIBUTION.

## Bucket boundaries matter
The API computes good service as the estimated count of values in the distribution that fall within `min` and `max`, so the result is an estimate when the threshold falls inside a bucket. For custom histograms, define a bucket boundary at the threshold.

## Gotchas
- If failed requests are measured by a separate availability SLO, filter the latency time series to avoid fast errors looking good.

## Checked
2026-10-31. Confirmed against the Monitoring API reference for ServiceLevelObjective and DistributionCut (DISTRIBUTION value type, DELTA or CUMULATIVE kind, estimated count between min and max, goal up to 0.9999, rolling period whole days up to 30), the `serviceLevelObjectives.create` method (POST path, `serviceLevelObjectiveId` query parameter), and the time-series selectors page (`select_slo_health`). Removed unconfirmed: load balancer and Cloud Run metric names and labels, Prometheus metric naming, Terraform resource, response-code filter and windows-based advice. 2419200s is 28 days.
Method: documentation only; no commands were run.

## Verify
- [ ] `services.serviceLevelObjectives` timeSeries selector `select_slo_health` shows plausible values vs Metrics Explorer p95.

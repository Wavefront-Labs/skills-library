---
id: computing-software.cloud-infrastructure-engineering.google-cloud.availability-slis-from-load-balancer-metrics
name: availability-slis-from-load-balancer-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, slo-monitoring, load-balancer-sli, availability-sli, good-total-ratio, https-lb-metrics]
level: practitioner
status: docs-checked
description: "Build availability SLIs from Application Load Balancer request counts with goodTotalRatio: choose good vs bad response classes, exclude client errors, and alert on burn rate."
sources: ["https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/sli-metrics/lb-metrics", "https://cloud.google.com/monitoring/api/metrics_gcp#gcp-loadbalancing", "https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Availability SLIs from load balancer metrics

The external ALB sees every request including those that never reach a healthy backend, so it is
the best source for user-facing availability.

## goodTotalRatio
```json
{
  "displayName": "checkout availability 99.9%",
  "goal": 0.999,
  "rollingPeriod": "<ROLLING_PERIOD>s",
  "serviceLevelIndicator": {"requestBased": {"goodTotalRatio": {
    "badServiceFilter": "metric.type=\"loadbalancing.googleapis.com/https/request_count\" resource.type=\"https_lb_rule\" resource.label.\"url_map_name\"=\"web-map\" metric.label.\"response_code_class\"=\"500\"",
    "totalServiceFilter": "metric.type=\"loadbalancing.googleapis.com/https/request_count\" resource.type=\"https_lb_rule\" resource.label.\"url_map_name\"=\"web-map\""
  }}}
}
```
Using `badServiceFilter` (5xx) + total counts 4xx as good, which is usually right (client errors are
not service failures). Exceptions: count 429 from your own rate limiting as bad if it reflects
capacity problems (filter `response_code="429"`).

## Choosing labels
- `response_code_class` is the label the docs use to split requests (the docs examples use `200`).
- Per-backend SLIs: use the `https/backend_request_count` metric with the `backend_target_name` resource label (as in the docs example).
- Internal ALB: `resource.type="internal_http_lb_rule"`, metric `loadbalancing.googleapis.com/https/internal_request_count`.

## Burn-rate alerts
```
select_slo_burn_rate("projects/<P>/services/checkout/serviceLevelObjectives/avail", "<FAST_WINDOW>s") > <FAST_THRESHOLD>
select_slo_burn_rate("projects/<P>/services/checkout/serviceLevelObjectives/avail", "<SLOW_WINDOW>s") > <SLOW_THRESHOLD>
```
Burn rate above 1 means the SLO will be missed if the error rate is sustained; the docs advise a threshold well above 1 for short windows. Page on the fast window, ticket on the slow one.

## Gotchas
- Cloud Armor denials (403) count as 4xx: good by this SLI; track Armor separately.
- Check how requests that get no response code are classed before relying on the ratio; inspect the `response_code_class` label values in Metrics Explorer.

## Verify
- [ ] Injected 5xx from a canary backend reduces SLI and burns budget at the expected rate.

## Checked
2026-10-28. Confirmed: SLI docs for load balancers (https_lb_rule and internal_http_lb_rule resource types, `https/request_count`, `https/internal_request_count`, `https/backend_request_count` with `backend_target_name`, `response_code_class` label, goodTotalRatio); Monitoring API v3 discovery (`TimeSeriesRatio` has `badServiceFilter`, `goodServiceFilter`, `totalServiceFilter`); burn-rate alerting page (`select_slo_burn_rate`, burn rate above 1 means out of SLO if sustained).
Fixed: internal ALB metric is `https/internal_request_count`, not `https/internal/request_count`; per-backend SLI uses `backend_request_count`.
Removed: 14.4 and 6 thresholds and window lengths, 2419200s period, `matched_url_path_rule`, `statusDetails`/`backend_timeout`, health-check claim, the code-0 label meaning.
Method: documentation only; no commands were run.

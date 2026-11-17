---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.window-based-vs-request-based-slos
name: window-based-vs-request-based-slos
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [window-based-slo, time-slice-slo, request-based-slo, slo, sli, error-budget]
level: practitioner
status: draft
description: "Choose between request-based (good/total events) and window-based (good minutes) SLOs, with PromQL for each and their behaviour under low traffic."
sources: ["https://sre.google/workbook/implementing-slos/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/", "https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/windows-based-slos"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Window-based vs request-based SLOs

## Definitions
- Request-based (occurrences): SLI = good events / valid events over the window. Every request counts equally.
- Window-based (time slices): split the window into slices (e.g. 1 min); a slice is good if it meets a criterion (error ratio < 1%, p99 < 300ms). SLI = good slices / total slices.

## PromQL
```promql
# request-based 30d availability
sum(increase(http_requests_total{code!~"5.."}[30d])) / sum(increase(http_requests_total[30d]))

# window-based: fraction of 1m slices with error ratio < 1% over 30d (subquery)
avg_over_time((
  (sum(rate(http_requests_total{code=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))) < bool 0.01
)[30d:1m])
```
For production, record the per-slice boolean with a recording rule every 1m and average the recorded series.

## Choosing
| Situation | Prefer |
|---|---|
| High, steady traffic; budget should scale with users hurt | request-based |
| Low or bursty traffic where one bad request should not burn 5% of budget | window-based |
| Latency percentile SLO ("p99 < 300ms") | window-based (percentiles are per-slice) |
| Contractual SLA phrased as uptime minutes | window-based |

## Gotchas
- Window-based hides severity: a slice at 1.1% errors and one at 100% count the same.
- Empty slices (no traffic) must be defined as good, bad or excluded; `< bool` on no data yields no sample, which `avg_over_time` silently excludes.
- Burn-rate alert maths from the Workbook assumes request-based; for slices, burn rate = bad-slice fraction / (1 - SLO).

## Verify
- [ ] SLO doc states the SLI type, slice length, slice criterion and empty-slice rule.
- [ ] Recorded slice series exists and the 30d SLI matches a manual calculation for one week.

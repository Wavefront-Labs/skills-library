---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.sli-recording-rules-and-error-budget-queries
name: sli-recording-rules-and-error-budget-queries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [sli-recording-rules, error-budget-remaining-query, recording-rules, slo, promql, burn-rate]
level: practitioner
status: verified
description: "Record SLI ratios at several windows with Prometheus recording rules and query remaining error budget, burn rate and budget consumed per day."
sources: ["https://sre.google/workbook/alerting-on-slos/", "https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/", "https://github.com/slok/sloth"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLI recording rules and error budget queries

## Rules
```yaml
groups:
  - name: slo-api-availability
    interval: 30s
    rules:
      - record: slo:sli_error:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{job="api",code=~"5.."}[5m]))
          / sum(rate(http_requests_total{job="api"}[5m]))
        labels: {slo: api-availability}
      - record: slo:sli_error:ratio_rate1h
        expr: |
          sum(rate(http_requests_total{job="api",code=~"5.."}[1h]))
          / sum(rate(http_requests_total{job="api"}[1h]))
        labels: {slo: api-availability}
      # repeat for 30m, 6h, 1d, 3d as needed by burn-rate alerts
      - record: slo:objective:ratio
        expr: vector(0.999)
        labels: {slo: api-availability}
```

## Queries
```promql
# burn rate over 1h (1 = spending exactly the budget)
slo:sli_error:ratio_rate1h{slo="api-availability"} / on(slo) (1 - slo:objective:ratio)

# 28d error ratio (average of 5m ratios is wrong under variable traffic; use counters)
sum(increase(http_requests_total{job="api",code=~"5.."}[28d])) / sum(increase(http_requests_total{job="api"}[28d]))

# remaining budget fraction (1 = untouched, <0 = overspent)
1 - (
  (sum(increase(http_requests_total{job="api",code=~"5.."}[28d])) / sum(increase(http_requests_total{job="api"}[28d])))
  / (1 - 0.999)
)
```

## Gotchas
- `avg_over_time(slo:sli_error:ratio_rate5m[28d])` weights quiet nights the same as peak hours; use counter increases for the long window.
- Divide-by-zero during no traffic yields NaN (tested: `vector(0)/vector(0) > 0.5` returns no series); alerts on NaN never fire, dashboards show gaps. That is usually acceptable; document it.
- Keep rule label sets identical across windows so `on(slo)` matches.

## Verify
- [ ] `promtool check rules` passes and `promtool test rules` has a case with a known burn rate.
- [ ] Remaining budget panel agrees with a hand calculation for a past incident.

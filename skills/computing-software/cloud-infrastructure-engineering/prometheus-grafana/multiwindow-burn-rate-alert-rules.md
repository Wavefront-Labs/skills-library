---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.multiwindow-burn-rate-alert-rules
name: multiwindow-burn-rate-alert-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [multiwindow-alert-rules, burn-rate-recording-rules, slo-based-alerting, multi-burn-rate, prometheus, alerting-rules]
level: advanced
status: verified
description: "Implement the SRE Workbook multiwindow multi-burn-rate alerts in Prometheus: recording rules per window, page and ticket thresholds, and promtool tests."
sources: ["https://sre.google/workbook/alerting-on-slos/", "https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://github.com/slok/sloth"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiwindow burn-rate alert rules

Workbook recommendation for a 30-day 99.9% SLO:
| Severity | Long window | Short window | Burn rate | Budget consumed |
|---|---|---|---|---|
| page | 1h | 5m | 14.4 | 2% |
| page | 6h | 30m | 6 | 5% |
| ticket | 3d | 6h | 1 | 10% |
The table is Table 5-8 of the SRE Workbook chapter "Alerting on SLOs" (99.9% SLO). The short window (1/12 of the long) makes the alert reset faster after recovery.

## Recording rules
```yaml
groups:
  - name: slo-api-burn
    rules:
      - record: slo:sli_error:ratio_rate5m
        expr: sum(rate(http_requests_total{job="api",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="api"}[5m]))
      # repeat for 30m, 1h, 6h, 3d with the window in the name
```

## Alerts
```yaml
  - name: slo-api-alerts
    rules:
      - alert: APIErrorBudgetBurnFast
        expr: |
          (slo:sli_error:ratio_rate1h > (14.4 * 0.001) and slo:sli_error:ratio_rate5m > (14.4 * 0.001))
          or
          (slo:sli_error:ratio_rate6h > (6 * 0.001) and slo:sli_error:ratio_rate30m > (6 * 0.001))
        for: 2m
        labels: {severity: page, slo: api-availability}
        annotations:
          summary: "API burning error budget fast ({{ $value | humanizePercentage }} errors)"
          runbook_url: https://runbooks.example.com/api-slo
      - alert: APIErrorBudgetBurnSlow
        expr: slo:sli_error:ratio_rate3d > 0.001 and slo:sli_error:ratio_rate6h > 0.001
        labels: {severity: ticket, slo: api-availability}
```

## Test
The rules above passed `promtool check rules` and were run with `promtool test rules` (Prometheus 3.15.0, 1 minute interval, 1000 requests per minute):
- Constant 2% errors from the first sample: the fast alert fires at 3 minutes (one evaluation interval plus `for: 2m`); a ticket alert is already firing.
- Healthy history, then 2% errors: the 1h window needs 14.4 x 0.001 = 1.44% of its minutes at 2%, so the fast alert fires only after roughly 45 minutes (not firing 45 minutes after the errors began, firing at 55), not at 5 minutes.
- Constant 0.2% errors: only `APIErrorBudgetBurnSlow` fires.
- 2% errors for 4h, then clean traffic: the fast alert resolves 20 to 22 minutes after recovery (the 6h/30m pair has to fall below 0.6%), and the slow ticket stays firing for at least 30 minutes.

## Gotchas
- `3d` windows over raw data are expensive: compute from 5m recorded ratios only if traffic is steady; otherwise record `increase` counters per hour and sum.
- Low traffic makes ratios jumpy; see low-traffic techniques before applying 14.4x on a few requests per minute.
- Generators (Sloth, Pyrra) produce exactly these rules; prefer them at scale.

## Verify
- [ ] promtool tests cover fast burn, slow burn, and recovery (the fast alert resolves once the 30m ratio drops below 6 x 0.001, about 21 minutes at 2% errors).

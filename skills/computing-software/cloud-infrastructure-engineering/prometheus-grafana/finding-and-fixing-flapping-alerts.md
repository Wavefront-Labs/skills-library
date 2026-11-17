---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.finding-and-fixing-flapping-alerts
name: finding-and-fixing-flapping-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [flapping-alerts, alert-flap-analysis, alert-fatigue, keep-firing-for, alerting-rules, alert-review-process]
level: practitioner
status: verified
description: "Find flapping alerts from ALERTS history and notification logs, then fix them with better windows, hysteresis, keep_firing_for or SLO-based rules."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://sre.google/workbook/alerting-on-slos/", "https://prometheus.io/docs/alerting/latest/configuration/#route"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding and fixing flapping alerts

A flapping alert fires and resolves repeatedly, creating many notifications for one underlying condition.

## Find them
```promql
# alerts with many state changes in a week (resets of the active-since timestamp)
topk(10, sum by (alertname) (changes(ALERTS_FOR_STATE[7d])))
```
`changes()` counts one per new episode after the first for each series (two firing episodes of one alert gave 1 in a `promtool test rules` run), so a count of N means about N+1 episodes per series, summed over series.
Also: paging tool reports (incidents auto-resolved in < 5 minutes), Alertmanager notification counts per group.

## Fixes, in order of preference
1. Replace threshold-on-noisy-metric with an SLO burn-rate alert (windows smooth noise by design).
2. Smooth the expression: longer `rate()` window, `avg_over_time(x[10m])`, `quantile_over_time`.
3. Hysteresis: fire above 90%, resolve only below 80% (tested with `promtool test rules`: fired at 10, held at 8.5, cleared at 7):
```yaml
expr: |
  disk_used_ratio > 0.9
  or (disk_used_ratio > 0.8 and on(instance) ALERTS{alertname="DiskAlmostFull", alertstate="firing"})
```
4. `keep_firing_for: 10m`: keeps the alert firing after the condition clears, preventing resolve/fire cycles (Prometheus 2.42+).
5. Increase `for` only if short spikes are genuinely harmless.
6. Alertmanager `group_interval`/`repeat_interval` reduce notification volume but do not fix the rule.

## Root causes to check
- Scrape failures making `up`-dependent expressions oscillate.
- Label changes (pod names) creating new alert identities.
- Thresholds set at normal peak levels.

## Verify
- [ ] The alert's episode count per week drops while still catching the test condition (promtool test with an oscillating series).

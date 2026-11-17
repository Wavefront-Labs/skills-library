---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.rule-group-limit-and-series-caps
name: rule-group-limit-and-series-caps
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [rule-group-limit, recording-rule-series-limit, recording-rules, alerting-rules, cardinality-limits]
level: practitioner
status: verified
description: "Cap the series a recording rule or alerts an alerting rule may produce with the rule group limit field, what happens on breach, and how to monitor it."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/#rule_group", "https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/#limiting-alerts-and-series", "https://grafana.com/docs/mimir/latest/references/configuration-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rule group limit

```yaml
groups:
  - name: per-route
    limit: 5000          # max series per recording rule / alerts per alerting rule in this group; 0 = no limit
    rules:
      - record: route:http_requests:rate5m
        expr: sum by (job, route) (rate(http_requests_total[5m]))
```

## Behaviour on breach (Prometheus docs, "Limiting alerts and series")
- Recording rule: all series produced by the rule in that evaluation are discarded (none written). The rule health is `err` with `exceeded limit of 3 with 5 series` (tested with limit 3).
- Alerting rule: all alerts for the rule, active, pending or inactive, are cleared (`ALERTS` returned nothing); error `exceeded limit of 2 with 5 alerts`.
- The evaluation is counted as failed: `prometheus_rule_evaluation_failures_total{rule_group=...}` increases (the `rule_group` label is `<file>;<group name>`) and the rule shows an error on the Rules page.

## Why use it
Protects storage and Alertmanager from a cardinality explosion in source data (a new high-cardinality label flowing into `sum by (route)`), and from alert storms of thousands of instances.

## Monitoring
```promql
increase(prometheus_rule_evaluation_failures_total[10m]) > 0
```
Alert on it (ticket severity), because a breached alerting rule silently stops alerting.

## Sizing
Set to 2-5x the normal output count (`count(route:http_requests:rate5m)`), not just above it.

## Gotchas
- Clearing alerts on breach means real alerts disappear during an explosion: prefer limits on recording rules, and generous limits on alerting rules.
- Mimir's ruler has its own per-tenant limits such as `ruler_max_rules_per_rule_group` (default 20) and `ruler_max_rule_groups_per_tenant` (Mimir configuration reference); they bound how many rules a group may hold, not how many series a rule produces.

## Verify
- [ ] Rule failures alert exists; a unit or staging test shows the breach behaviour.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), jq 1.8.2, Git Bash tar.
- Groups with `limit: 3` (a recording rule producing 5 series), `limit: 100` (same rule) and `limit: 2` (alerting rule producing 5 alerts): `/api/v1/rules` showed health `err` with `exceeded limit of 3 with 5 series` and `exceeded limit of 2 with 5 alerts`; the over-limit recording rule's output series were absent, the `limit: 100` group stored 5 series; `prometheus_rule_evaluation_failures_total` rose per group. The skill's group YAML (limit 5000) passes `promtool check rules`; `limit` semantics and default 0 come from the 3.15 recording-rules page.
- Mimir limit names and the default of 20: Mimir configuration reference. The Mimir ruler was not run.

---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-route-tree-design
name: alertmanager-route-tree-design
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [route-tree-design, continue-routing, alertmanager, alert-routing, amtool-config-routes-test]
level: practitioner
status: verified
description: "Design an Alertmanager route tree: top-level defaults, team/severity branches, matchers, continue for fan-out, and testing routes with amtool."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/#route", "https://prometheus.io/docs/alerting/latest/configuration/#matcher", "https://github.com/prometheus/alertmanager#amtool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager route tree design

An alert enters at the root route and descends into the **first** matching child (depth first). Without `continue: true`, matching stops there. Children inherit unset parameters (receiver, group_by, timings) from the parent.

## Pattern: team then severity
```yaml
route:
  receiver: default-ticket          # catch-all: never lose an alert
  group_by: [alertname, cluster, namespace]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    # audit copy of every page to a chat channel, then continue to the real route: FIRST child
    - matchers: [severity="page"]
      receiver: pages-firehose
      continue: true
    - matchers: [alertname="Watchdog"]
      receiver: deadmansswitch
      repeat_interval: 1m
    - matchers: [team="payments"]
      receiver: payments-ticket
      routes:
        - matchers: [severity="page"]
          receiver: payments-pager
    - matchers: [team="platform"]
      receiver: platform-ticket
      routes:
        - matchers: [severity="page"]
          receiver: platform-pager
```
The audit route (`severity="page"`, receiver `pages-firehose`, `continue: true`) must be the first child. When it was the last child it never saw team pages: `amtool config routes test team=payments severity=page alertname=X` returned only `payments-pager` (the first matching sibling stops the walk), and only pages without a team label reached the firehose. Moved to the top of `routes:`, the same test returned `pages-firehose,payments-pager` and `severity=page alertname=Y` returned `pages-firehose`. So put `continue: true` audit routes before routes that would stop matching if you want them to see everything.

## Matchers
`matchers: ['severity=~"page|critical"', 'env!="dev"']` (the current syntax; the configuration docs mark `match`/`match_re` DEPRECATED). Quote values with special characters. `mute_time_intervals` and `active_time_intervals` are not inherited by children, while `receiver`, `group_by`, `group_wait`, `group_interval` and `repeat_interval` are (docs).

## Testing
```bash
amtool check-config alertmanager.yml
amtool config routes show --config.file=alertmanager.yml
amtool config routes test --config.file=alertmanager.yml team=payments severity=page alertname=X
# expected output: payments-pager   (run on amtool 0.34.1; with the audit route first: pages-firehose,payments-pager)
```
Other results run against this tree: `alertname=Watchdog` gave `deadmansswitch`, `team=platform severity=warning` gave `platform-ticket`, `foo=bar` gave `default-ticket`; `--tree` prints the matching routes.
Put a table of label sets and expected receivers in CI.

## Gotchas
- Alerts without a `team` label go to the root receiver: monitor that receiver's volume.
- `group_by: ['...']` aggregates by all labels, which in practice means one group per distinct label set (configuration docs); use only for already-aggregated alerts.
- Deep trees with regexes become unreadable; prefer consistent labels set by rules.

## Verify
- [ ] Route test table passes in CI; root receiver gets under 5% of alerts (a target, not a measured figure).

## Checked
Alertmanager and amtool 0.34.1 (windows-amd64) run locally: `check-config` and `config routes show` on the skill's tree (7 webhook receivers), `routes test` for five label sets, `--verify.receivers` match and mismatch, `--tree`, and the same tests after moving the audit route to the first position. Docs read: Alertmanager configuration.md (route inheritance, `continue`, deprecated `match`/`match_re`, `group_by: ['...']`).

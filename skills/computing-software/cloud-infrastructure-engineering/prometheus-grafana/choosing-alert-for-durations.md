---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.choosing-alert-for-durations
name: choosing-alert-for-durations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [for-duration-choice, pending-state, alerting-rules, for-clause, alert-fatigue, keep-firing-for]
level: practitioner
status: verified
description: "Pick for: durations per alert type, understand pending state, restarts (ALERTS_FOR_STATE restore) and how for interacts with evaluation and scrape intervals."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing for durations

`for: 5m` keeps an alert in **pending** until the expression has been true at every evaluation for 5 minutes, then it fires. One false evaluation resets it to inactive.

## Guidance (rules of thumb, not from a standard)
| Alert type | for | Why |
|---|---|---|
| Multiwindow burn-rate (fast) | 1-2m | windows already smooth noise; page quickly |
| Burn-rate (slow) | 15m-1h or none with long windows | ticket |
| Target down (`up == 0`) | 5m | rides out restarts and single scrape failures |
| Resource forecast (disk full in 4h) | 30m-1h | trend must persist |
| Watchdog | none | always firing |
| Absent metric | 10-15m | allow for deploys |

## Mechanics
- Minimum effective delay = `for` + up to one evaluation interval + scrape interval + Alertmanager `group_wait`.
- `for` smaller than the evaluation interval behaves like the evaluation interval (tested: `for: 10s` with a 1m interval fired at the second evaluation). With `for: 5m` and the first true evaluation at 1m, the alert was still pending at 5m and firing at 6m.
- Flapping expressions never reach firing with long `for`: use `keep_firing_for` for flapping resolution, or smooth the expression (`avg_over_time`, longer rate windows) rather than raising `for` indefinitely.

## Restarts
Prometheus restores pending/firing state after restart from `ALERTS_FOR_STATE` if the outage was shorter than `--rules.alert.for-outage-tolerance` (default 1h), and applies `--rules.alert.for-grace-period` (default 10m), the minimum duration between the alert and its restored `for` state, only to alerts whose `for` is greater than the grace period (flag help, Prometheus 3.15.1).

## Gotchas
- Long `for` on high-severity alerts delays pages: SLO burn-rate design is usually better than "error rate > X for 15m".

## Verify
- [ ] promtool test cases cover pending vs firing at the `for` boundary.

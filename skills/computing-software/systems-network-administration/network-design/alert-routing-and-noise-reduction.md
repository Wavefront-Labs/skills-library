---
id: computing-software.systems-network-administration.network-design.alert-routing-and-noise-reduction
name: alert-routing-and-noise-reduction
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, monitoring, alert-fatigue, alert-routing, dependency-suppression, on-call]
level: practitioner
status: draft
description: "Cut network alert noise: alert only on actionable symptoms, parent/child dependency suppression, hysteresis and flap damping, deduplication and routing to the right team."
sources:
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://prometheus.io/docs/alerting/latest/alertmanager/
  - https://docs.librenms.org/Alerting/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alert routing and noise reduction

## Principles
- Page only for **actionable, user-impacting** conditions (site down, core link down without
  redundancy, internet loss); everything else is a ticket or a dashboard.
- Every alert has an owner, severity and runbook link.
- Review alert volume weekly: delete or tune any alert nobody acts on.

## Techniques
| Technique | Example |
|---|---|
| Dependency/parent suppression | site router down -> suppress all access switches/APs behind it (LibreNMS parent devices, Zabbix dependencies, Alertmanager inhibit rules) |
| Hysteresis / duration | alert when utilisation > 90 % for 15 min, clear below 80 % |
| Flap damping | interface flapping: one alert "flapping" instead of 50 up/down |
| Deduplication and grouping | Alertmanager `group_by: [site]` -> one notification per site |
| Maintenance windows | silence during approved changes automatically from the change system |
| Redundancy awareness | one member of a redundant pair down = ticket (P3), both down = page (P1) |

## Routing
- By severity: P1 page via PagerDuty/Opsgenie; P2 chat channel; P3 ticket.
- By ownership: WAN circuits to network team plus carrier ticket automation; DC power to facilities.
- After-hours rules differ from business hours for non-critical sites.

## Alertmanager inhibition example
```
inhibit_rules:
- source_matchers: [alertname="SiteDown"]
  target_matchers: [severity=~"warning|critical"]
  equal: [site]
```

## Verify
- [ ] Pages per on-call week trend down; > 80 % of pages led to action; a site outage produces one page, not dozens.

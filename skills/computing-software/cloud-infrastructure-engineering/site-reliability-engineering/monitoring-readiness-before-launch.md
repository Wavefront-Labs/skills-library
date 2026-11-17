---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.monitoring-readiness-before-launch
name: monitoring-readiness-before-launch
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, production-readiness, launch-monitoring-readiness, slo-monitoring, alerting, dashboards]
level: practitioner
status: draft
description: "Confirm monitoring readiness before launch: SLIs and SLOs live, paging alerts with runbooks, dashboards, logs and traces, synthetic checks, and an on-call rotation in place."
sources: ["https://sre.google/sre-book/launch-checklist/", "https://sre.google/workbook/monitoring/", "https://sre.google/sre-book/monitoring-distributed-systems/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitoring readiness before launch

**Goal:** if the launch goes wrong, the team finds out from monitoring before users tell them.

## Checklist
**SLIs/SLOs**
- [ ] SLIs for the critical user journeys defined and recorded (availability, latency, freshness as relevant).
- [ ] SLO targets agreed; burn-rate alerts (fast and slow) configured.

**Alerting**
- [ ] Paging alerts limited to user-impacting symptoms; each has a runbook and a test firing.
- [ ] Ticket-level alerts for capacity (disk, quota usage, certificate expiry).
- [ ] Alerts route to the correct on-call rotation; escalation tested.

**Visibility**
- [ ] Service dashboard: RED per endpoint, saturation, dependencies, deploy annotations.
- [ ] Launch dashboard combining business metrics (signups, orders) with health.
- [ ] Logs structured and searchable; traces with propagation through all services; exemplars linked.

**External view**
- [ ] Synthetic checks from multiple regions on key journeys.
- [ ] Status page component exists.

**People**
- [ ] On-call rotation staffed (primary and secondary) through the launch window; launch war-room roles assigned.
- [ ] Rollback procedure documented and rehearsed.

## Dry run
Inject a fault in staging or pre-prod (kill dependency, add latency) and confirm: alert fires within expected time, runbook leads to mitigation, dashboards show the problem.

## Verify
- [ ] Checklist signed in the launch review; dry-run results recorded.

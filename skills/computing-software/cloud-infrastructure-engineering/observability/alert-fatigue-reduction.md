---
id: computing-software.cloud-infrastructure-engineering.observability.alert-fatigue-reduction
name: alert-fatigue-reduction
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, alerting, alert-fatigue, alert-noise, pager-fatigue, on-call-health, actionable-alerts, symptom-based-alerting, cause-based-alerts, alert-audit, alert-review, deduplication, grouping, inhibition, silences, alertmanager, pagerduty, opsgenie, event-intelligence, routing, severity, page-vs-ticket, flapping, hysteresis, for-duration, runbook-links, alert-ownership, signal-to-noise]
level: practitioner
status: draft
description: "Cut alert noise: audit every alert for actionability, page only on user-facing symptoms, route the rest to tickets, group/inhibit/dedupe in Alertmanager or PagerDuty, and review noise weekly."
sources: ["Google SRE Book - Monitoring Distributed Systems", "Rob Ewaschuk - My Philosophy on Alerting", "Prometheus Alertmanager documentation", "PagerDuty documentation - Alert grouping and noise reduction"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alert fatigue reduction — every page is real, urgent and actionable

**Goal:** on-call engineers trust the pager: each page means users are (or will shortly be)
hurt and a human must act now. Everything else goes somewhere quieter.

## 1. Audit what you have
Export 30 days of alerts (Alertmanager/PagerDuty/Opsgenie analytics). For each alert rule record:
fires/month, % acknowledged then resolved with **no action**, median time-to-ack, after-hours count, owner.
Classify every rule into one of:
- **Page** — user impact now or imminent, needs human action within minutes.
- **Ticket** — needs action within days (disk 70% full, cert expires in 14 days, replica lagging but within SLO).
- **Dashboard/log only** — informational; no one acts on it.
- **Delete** — nobody knows why it exists, or it duplicates a better alert.
Teams typically find that a large share of pages (often half or more — measure yours) fall in the last three groups.

## 2. Page on symptoms, not causes
- Symptoms: SLI burn rate, error rate on a user journey, synthetic check failing, queue age beyond deadline. These capture every cause, including ones you didn't predict.
- Causes (CPU 90%, pod restarted, one node down) become tickets or dashboard signals — unless they reliably predict imminent user impact that the symptom alerts would catch too late (e.g. disk will fill in < 4 h).
- Prefer **SLO burn-rate pages** over static thresholds; see
  `computing-software.cloud-infrastructure-engineering.observability.slo-based-alerting`.

## 3. Make each page actionable
Every paging rule must have: owner team, severity, a summary with the affected service and
impact, a **runbook link** with first steps, and dashboard link. No runbook → it isn't ready to page.
```yaml
annotations:
  summary: "Checkout error budget burning 14x ({{ $labels.region }})"
  runbook_url: "https://runbooks.example.internal/checkout/burn-rate"
  dashboard: "https://grafana.example.internal/d/checkout-slo"
```

## 4. Reduce duplicates mechanically
- **for:** durations (e.g. `for: 5m`) to skip transient blips; add hysteresis (different fire and resolve thresholds) to stop flapping.
- **Grouping:** Alertmanager `group_by: [alertname, service, region]`, `group_wait: 30s`, `group_interval: 5m`, `repeat_interval: 4h` — one notification per incident, not per pod.
- **Inhibition:** suppress downstream alerts when an upstream one is firing (region down inhibits per-service alerts in that region; cluster unreachable inhibits pod alerts).
- **Dependencies:** PagerDuty/Opsgenie event orchestration or intelligent grouping to merge related alerts into one incident.
- **Silences** for planned maintenance, created by the change process with an expiry — never open-ended.

## 5. Route deliberately
Page the team that can fix it, not a central NOC that forwards it. Low-severity routes go to a
ticket queue or team channel with a daily triage owner. Business-hours-only routing for anything that can wait until morning.

## 6. Keep it clean
- Weekly on-call handoff reviews the noisiest 5 alerts; each gets fixed, downgraded or deleted with an owner.
- Track: pages per shift, after-hours pages, % actionable. Set a target (e.g. ≥ 90% actionable; ≤ 2 incidents per 12-h shift).
- New alerts start as ticket severity and get promoted to page after proving they're actionable.

## Gotchas
- Raising thresholds to cut noise often just delays real pages; fix the signal (symptom-based) instead.
- Silencing a noisy alert "temporarily" without expiry is deleting it with no review.
- One alert per instance in autoscaled fleets scales noise with traffic; aggregate across the fleet.
- Alerts on metrics that disappear (scrape fails) never fire — add `absent()` / staleness alerts for critical SLIs.

## Verify
- [ ] Every paging rule has owner, severity, runbook and dashboard links.
- [ ] Last 30 days: % of pages requiring action ≥ the team's target.
- [ ] Grouping and inhibition rules exist for the main failure domains.
- [ ] Weekly noisy-alert review produced changes in the last month.
- [ ] Critical SLIs have absent-data alerts.

Uncertain: the noise and per-shift figures are common guidance, not measured benchmarks for your org.

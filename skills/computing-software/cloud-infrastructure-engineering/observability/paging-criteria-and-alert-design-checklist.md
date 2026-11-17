---
id: computing-software.cloud-infrastructure-engineering.observability.paging-criteria-and-alert-design-checklist
name: paging-criteria-and-alert-design-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [alerting, paging-criteria, ticket-alerts, alert-quality-checklist, alert-design-checklist, symptom-based-alerting, sre-book]
level: practitioner
status: draft
description: "Decide what pages vs what becomes a ticket, using the SRE Book's paging questions, and review every new alert against a design checklist before it ships."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://sre.google/workbook/alerting-on-slos/", "https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paging criteria and the alert design checklist

## Three outputs, not one
| Output | When | Example |
|---|---|---|
| **Page** | a human must act now; users are or will soon be affected | SLO fast burn, total outage, data loss risk |
| **Ticket** | must be done, but in hours/days | SLO slow burn, disk fills in 3 days, cert expires in 14 days |
| **Log/dashboard only** | diagnostic, no action required | single pod restart, CPU 80 % |

## The SRE Book paging questions
Before an alert can page, answer yes to all:
1. Does it detect an otherwise undetected condition that is **urgent, actionable, and user-visible** (or imminently so)?
2. Will I ever be able to ignore it, knowing it's benign? If yes, fix the rule.
3. Does it definitely indicate users are being negatively affected? Cases where they aren't (drained
   traffic, test deployments) must be filtered out.
4. Can I take action in response? Is it urgent or can it wait until morning?
5. Are other people getting paged for the same issue (redundant pages)?
Pages should be about a novel problem; if the response is robotic, automate it instead.

## Design checklist (review on every PR adding an alert)
- [ ] Symptom-based (error ratio, latency, availability) rather than cause (CPU, one pod down), unless the cause
  predicts imminent user impact (disk full, cert expiry).
- [ ] Tied to an SLO or a named user journey where possible.
- [ ] `for:` duration set to avoid blips; burn-rate windows for SLO alerts.
- [ ] Severity label maps to page/ticket/info, with an owning `team`.
- [ ] Summary says what is broken for whom; description says what to check first.
- [ ] `runbook_url` exists and the runbook has a first-five-minutes section.
- [ ] Tested (`promtool test rules`) with firing and non-firing cases.
- [ ] Backtested against 2-4 weeks of history: how often would it have fired? Each firing actionable?
- [ ] No duplicate of an existing alert at a different threshold (use inhibition instead).
- [ ] Low-traffic guard where ratios can be noisy.

## Verify
- [ ] Every paging alert in the repo passes the five questions (record the answers in the PR).
- [ ] Ticket-severity alerts route to a queue, not to the pager.

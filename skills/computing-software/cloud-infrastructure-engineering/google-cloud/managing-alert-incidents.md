---
id: computing-software.cloud-infrastructure-engineering.google-cloud.managing-alert-incidents
name: managing-alert-incidents
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alerting, alert-incidents, incident-acknowledge, documentation, on-call]
level: practitioner
status: docs-checked
description: "Work Cloud Monitoring alerts day to day: acknowledge, understand auto-close, write policy documentation with variables and runbook links, and review alert history."
sources: ["https://cloud.google.com/monitoring/alerts/incidents-events", "https://cloud.google.com/monitoring/alerts/doc-variables", "https://cloud.google.com/monitoring/alerts/manage-incidents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing alert incidents

## 1. Incident lifecycle
States: **Open** → **Acknowledged** (manually marked, typically while the alert is being investigated) → **Closed**
(condition cleared or auto-close). Console: Monitoring → Alerting.
- Mark an alert acknowledged when you begin investigating the cause.
- Auto-close applies when no observations arrive for the policy's auto-close duration; configure it in the console or API.

## 2. Documentation that helps at 3 a.m.
```yaml
documentation:
  subject: "5xx rate high"
  content: |
    5xx class ${metric.label.response_code_class} above threshold.
    Runbook: <RUNBOOK_URL>
  links: [{displayName: Runbook, url: "<RUNBOOK_URL>"}]
```
Documentation has a subject, content and links, supports Markdown, and `${metric.label.KEY}` style variables (see the documentation-variables page for the full list).

## 3. Routing and review
- Route notifications per team with notification channels on each policy.
- Review alert history for postmortems and noisy-alert reviews.
- Monthly: top 10 noisiest policies by incident count → tune or delete.

## Gotchas
- Monitoring does not open alerts while a policy is snoozed or disabled; use a snooze to silence a known issue.
- Prefer disabling a policy over deleting it during investigations, so context is kept.

## Verify
- [ ] A test alert shows rendered documentation with working links.

## Checked

2026-10-28. Confirmed against: Monitoring alerts incidents-events page (Acknowledged meaning, auto-close, snoozed or disabled policies do not open alerts) and the documentation-variables page (subject, content, links, metric.label.KEY).

Removed or rewritten: renotify and PagerDuty ack-sync claims, reopen-on-manual-close, severity enum, mimeType, policy.user_labels and other variables from the example, user-label routing, and the deleted-policy-closes-incidents claim.

Method: documentation only; no commands were run.

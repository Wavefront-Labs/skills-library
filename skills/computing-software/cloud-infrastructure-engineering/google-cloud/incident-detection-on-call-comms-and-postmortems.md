---
id: computing-software.cloud-infrastructure-engineering.google-cloud.incident-detection-on-call-comms-and-postmortems
name: incident-detection-on-call-comms-and-postmortems
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, incident-management, incident-detection, alert-to-incident, on-call-rotation, escalation-policies, status-page, customer-communication, postmortem-template, action-item-tracking, personalized-service-health]
level: practitioner
status: docs-checked
description: "Run incidents the SRE way on Google Cloud: alerts to declared incidents, on-call rotations and escalation, status comms incl. Personalized Service Health, blameless postmortems."
sources: ["https://sre.google/workbook/incident-response/", "https://sre.google/sre-book/managing-incidents/", "https://sre.google/sre-book/postmortem-culture/", "https://cloud.google.com/service-health/docs/overview", "https://cloud.google.com/monitoring/alerts/incidents-events"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident detection, on-call, comms and postmortems

## 1. From alert to incident
- Page only on **symptoms users feel** (SLO burn-rate alerts, uptime checks), not on every cause metric.
- Declare an incident when any is true (SRE book guideline): you need to involve a second team, the outage is visible to customers, or the issue is unsolved after an hour of concentrated analysis. Declare early: the SRE book says it is better to declare early and close out than to start the framework hours into a growing problem.
- Roles (SRE workbook): Incident Commander (IC), Communications Lead, Operations Lead; the CL and OL report to the IC. Larger responses also use a scribe. The person who declares typically becomes IC; hand over explicitly.
- Cloud Monitoring alerts: mark an alert as acknowledged when you begin investigating (Google recommends this), so others see it is being worked. The alerting policy's documentation section appears on the alert, so put the runbook link there.

## 2. Is it Google?
Check **Personalized Service Health**, which shows Google Cloud service health events relevant to your projects, before deep-diving. Its alerts are based on logs in Cloud Logging, so they can be routed next to your own alerting.
```bash
gcloud beta service-health events list --location=global --project=<P>
```

## 3. On-call
- Primary plus secondary, follow-the-sun where possible; weekly handoff with open-issue review.
- Notification channels: your paging tool through the Monitoring integration or a webhook; define an escalation policy before you need it.
- Track pages per shift; frequent actionable pages mean the alerting or system needs work.

## 4. Communication
Update on a fixed rhythm and on change: *what is affected, since when, current status, next update time*.
Agree the channel beforehand (the workbook advises choosing one the team already knows) and keep
a live incident document. External: status page (component status, no speculation). Close with an
all-clear and a postmortem promise.

## 5. Blameless postmortem
Template: summary, impact (users, duration, SLO budget burned), timeline (UTC), root cause and
trigger, detection (how/when), what went well/badly/lucky, **action items** (owner, priority, due,
ticket link). The SRE book says an unreviewed postmortem might as well never have existed: hold
regular review sessions. Track action items in the normal backlog with a label and report
completion regularly; postmortems without closed actions repeat.

## Gotchas
- Mixing debugging and comms in one person's hands slows both; split roles even for small incidents.
- "Root cause: human error" is not a root cause; ask why the system allowed it.
- Check the incident list in Monitoring after a page; follow-on alerts may be grouped into it.

## Verify
- [ ] Every page in the last quarter maps to an alert with a runbook link.
- [ ] Every postmortem action item has an owner and due date and is tracked to closure.

## Checked
2026-10-31. Confirmed against the SRE book (Managing Incidents, Postmortem Culture), the SRE workbook (Incident Response), the Personalized Service Health overview and the Cloud Monitoring incidents and events page: declaration criteria, IC/CL/OL roles, acknowledging alerts, documentation section on alerts, alerts based on Cloud Logging logs, blameless postmortem and review guidance. `gcloud beta service-health events list` and its flags were checked against the gcloud reference by check_commands.py. Removed unconfirmed figures: rotation size, escalation timings, pages-per-shift threshold, comms interval, 5-day review window, 80% closure target, and the Pub/Sub routing and support-case claims.
Method: documentation only; no commands were run.

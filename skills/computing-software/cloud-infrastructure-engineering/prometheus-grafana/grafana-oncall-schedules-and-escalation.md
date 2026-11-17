---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-oncall-schedules-and-escalation
name: grafana-oncall-schedules-and-escalation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-oncall, grafana-irm, oncall, on-call, oncall-schedules, rotations, shifts, overrides, escalation-chains, escalation-policies, integrations, alertmanager-integration, grafana-alerting-integration, routes, notification-rules, mobile-app, slack-integration, chatops, ical-export, shift-swaps, oncall-terraform, incident-management, pagerduty-alternative]
level: practitioner
status: docs-checked
description: "Grafana OnCall routes, escalation chains and step types, web schedules with rotations, overrides, quality score, iCal export and shift swaps."
sources: ["https://github.com/grafana/oncall/blob/dev/docs/sources/configure/escalation-chains-and-routes/index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/manage/on-call-schedules/_index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/manage/on-call-schedules/web-schedule/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana OnCall schedules and escalation

**Goal:** the right human is paged, escalating automatically if nobody reacts, from a schedule people can see in their
calendars.

## 1. Routes
A route picks the escalation chain for an alert group using a routing template (Jinja). The **first matching route**
wins, and the template must evaluate to True. Manage routes on the Integrations page (Add route / Edit): pick the
escalation chain, choose ChatOps channels under Publish to ChatOps, and reorder with the up/down arrows because order
decides evaluation. Examples from the docs:
```
{{ payload.severity == "critical" and payload.service == "database" }}
{{ "synthetic-monitoring-dev-" in payload.namespace }}
```
Label-based routing (`labels.foo`) is Grafana Cloud only.

## 2. Escalation chains
A chain runs until a user acknowledges, resolves or silences the alert group. Create it on the Escalation Chains
page: unique name across the organisation, assigned to a team (alert groups inherit the team from the integration, not
the chain). Changing a chain affects every linked integration and route. Step types in the docs: Wait, Notify users,
Notify users from on-call schedule, Notify all team members, Resolve incident automatically, Notify Slack channel
members, Notify Slack user group, Trigger outgoing webhook, Round robin notifications, Time-based escalation,
Threshold-based escalation, Repeat escalation (loops the chain up to five times), and Declare incident (Cloud only, one
incident per route at a time).
The two Slack steps notify OnCall-registered users through their notification rules and do not post in the alert
group's Slack thread. Each step selects Default or Important personal notification rules.

## 3. Schedules
- Admin and Editor roles can create, edit and delete schedules; Viewers cannot receive notifications, so cannot be
  on call.
- Three kinds: web-based (built in), iCal import (read-only in OnCall), and Terraform-managed (also read-only in the UI).
- Schedule settings (gear icon): Slack channel, Slack user group, notification frequency, action for a slot when no one
  is on call, current-shift and next-shift notification settings.
- The schedule view shows Final schedule (rotations plus overrides), Rotations, and Overrides; override events take
  precedence over rotations.
- Quality report: score 0-100 from gaps (time with nobody on call) and balance (uneven load); scale 0-20 Bad, 20-40
  Low, 40-60 Medium, 60-80 Good, 80-100 Great. It looks at the next 52 weeks and can list the percentage not covered and
  overloaded users ("+15% avg" means 15% more on-call time than average).
- Export to a calendar app with a one-time secret iCal URL.
- Shift swap requests let a teammate volunteer to take your shifts for a period.

## Verify
- [ ] Every route order was tested with a sample payload; the first matching route is the intended one.
- [ ] Schedule quality shows no uncovered time.
- [ ] Every escalation chain ends with a step that reaches a human.

## Checked

2026-11-08. Confirmed against the raw OnCall docs in the grafana/oncall repository: configure/escalation-chains-and-routes,
manage/on-call-schedules (index and web-schedule). The grafana.com URLs redirect to a generic landing page, so these
repository files replaced them in `sources`. Removed as unconfirmed: Alertmanager and Grafana Alerting integration
templates, the Terraform resource examples (registry pages were unreadable), personal notification rule examples, the
day-2 API/heartbeat/maintenance section, and the gotchas list.
Method: documentation only; no commands were run.

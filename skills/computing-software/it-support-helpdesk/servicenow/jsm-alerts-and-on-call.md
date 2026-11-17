---
id: computing-software.it-support-helpdesk.servicenow.jsm-alerts-and-on-call
name: jsm-alerts-and-on-call
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, jsm-alerts, jira-service-management, on-call, opsgenie, alert-routing, escalation-policy]
level: practitioner
status: draft
description: "Configure Jira Service Management alerts and on-call: integrations, alert routing, on-call schedules, escalation policies, and linking alerts to incidents."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/what-are-alerts/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/what-is-on-call-schedule/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/what-are-escalation-policies/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-alerts-and-on-call

JSM includes the Opsgenie capabilities (alerts, on-call, escalations) under Operations.

## Alerts
- Sources: monitoring integrations (Datadog, Azure Monitor, CloudWatch, email, API).
  Each integration is owned by a team and maps alert fields (priority, tags, responders).
- Deduplication: alerts with the same **alias** increment a count instead of creating new
  alerts; set alias from host + check name in the integration.
- Alert actions: acknowledge, close, add note, escalate, create incident.
- Use alert policies to suppress noise (maintenance windows) and to set priority.

## On-call schedules
- Team > On-call: create a schedule with rotations (weekly, daily), participants, time
  zone, and handover time. Add overrides for holidays and swaps.
- Users install the mobile app and set notification rules (push, SMS, voice) with delays;
  test with "Send test notification".

## Escalation policies
- Example: notify on-call user immediately; if not acknowledged in 5 min notify next in
  rotation; at 15 min notify team lead; at 30 min notify all team members.
- Routing rules on the team decide which escalation applies by alert priority/tags and
  time of day.

## Alerts to incidents
- A P1/P2 alert can create a JSM incident (major incident workflow, stakeholder
  updates, conference bridge) automatically or by an action.
- Link related alerts to the incident; closing the incident doesn't close alerts unless
  configured.

## Pitfalls
- Everyone notified for everything: alert fatigue and ignored pages.
- Schedules in the wrong time zone at handover.
- Personal notification rules never configured, so pages go only to email.

## Verify
A test alert from each integration routes to the right team, pages the current on-call,
escalates when not acknowledged, and shows in the alert history.

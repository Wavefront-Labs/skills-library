---
id: computing-software.it-support-helpdesk.servicenow.sla-warning-and-breach-escalation
name: sla-warning-and-breach-escalation
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, sla, service-level-management, sla-escalation, sla-breach, sla-workflow, sla-flow, at-risk-tickets, breach-notification]
level: practitioner
status: draft
description: "Act before SLAs breach: 50/75/100% notifications via SLA flows, at-risk dashboards, escalation to leads, and handling and reporting breaches honestly."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sla-warning-and-breach-escalation

Goal: the people who can help hear about a ticket while there's still time
to meet the SLA — not after it breached.

## Notifications at thresholds
ServiceNow SLA definitions run an **SLA flow** (Flow Designer; legacy: SLA
workflow) — the default flow notifies at 50 %, 75 % and 100 % (breach) of
duration. Typical:
| Threshold | Notify |
|---|---|
| 50 % | assigned agent (or group if unassigned) |
| 75 % | agent + group manager/team lead |
| 100 % | team lead + service owner; P1/P2 also duty manager |
Customise by priority; P1 notifications by SMS/Teams, not just email.

## At-risk view
Dashboard/list of task SLAs where `stage=in_progress` and
`business_percentage >= 60`, sorted by time left — the shift lead's first
screen. Agents: "My work" sorted by SLA due, not by ticket number.

## Escalation actions at 75 %
- Is it assigned to a person? If not, assign.
- Blocked? Escalate the blocker (vendor/other team) explicitly.
- Can't make it? Tell the user before the deadline, with a new expected
  time and reason — a broken promise communicated early hurts far less.
- Consider swarming or reassignment to someone with time.

## After a breach
- Don't manipulate states/pauses to undo it.
- Record a breach reason (field or work note): capacity, vendor, waiting on
  change, misprioritised, routing delay.
- Breach reasons feed the monthly service review; recurring reasons →
  problem/improvement actions.

## Gotchas
- Notification fatigue: too many 50 % emails get filtered — keep early
  thresholds to the assignee in-tool notifications.
- Paused SLAs don't notify — ensure pending tickets have follow-up dates.

## Verify
Breach rate trend and share of breaches with recorded reasons; spot-check
that 75 % notifications reached a lead for recent breaches.
